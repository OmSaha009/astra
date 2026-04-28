import re
import sympy as sp
import os, tempfile
from memory import db_utils
from ocr_module import LatexOCRModel
from ocr_module.latex_sanitizer import LatexSanitizer
from core.logging import setup_logger
from typing import Annotated, Optional
from core.intent import classify_intent
from tools import sandbox, code_extractor
from core.task_extractor import extract_best
from core.responders.steps_responder import generate_steps
from core.responders.math_responder import generate_math_response
from core.responders.chat_responder import generate_chat_response
from core.responders.study_responder import generate_study_response
from core.streaming import stream_generator_math, stream_generator_other
from fastapi import FastAPI, UploadFile, Form, Request, File, APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse, Response, PlainTextResponse

logger = setup_logger(__name__)
router = APIRouter()



@router.post("/message-response")
async def handle_message(
    message: Annotated[str, Form()],
    subject: Annotated[str, Form()],
    image: Optional[UploadFile] = File(None),
    pdf: Optional[UploadFile] = File(None),
    session_id: Optional[str] = Form(None)
    ):

    logger.info(f"Message received: {message[:50]}...")

    if not session_id:
        session_id = db_utils.create_session()
    logger.info(f"Session ID: {session_id}")

    latex_from_image = None
    if image:
        try:
            model = LatexOCRModel()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                content = await image.read()
                tmp.write(content)
                tmp_path = tmp.name
            latex_from_image = model.predict(tmp_path)
            os.unlink(tmp_path)
            logger.info(f"OCR extracted: {latex_from_image[:50]}...")
            if not message.strip():
                message = latex_from_image
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            

    db_utils.save_message(session_id=session_id, role="user", content=message)

    history = db_utils.get_recent_messages(session_id=session_id, limit=10)

    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])


    if subject == "Chemistry":
        logger.info("Chemistry module - returning placeholder")
        return {"response": "Chemistry module coming soon"}



    int_conf = classify_intent(message)

    task_topic = ""
    if int_conf["intent"] == "chat":
        task_topic = {"task": "conversation", "topic": message}
    else:
        task_topic = extract_best(message)

    try:


        if int_conf["intent"] == "math_solve":
            response = generate_math_response(message, context, task_topic["task"], task_topic["topic"])
        elif int_conf["intent"] == "chat":
            response = generate_chat_response(message, context)
        else:  # study
            response = generate_study_response(message, context, task_topic["topic"])

        
        
        full_response = ""

        if int_conf["intent"] == "math_solve":

            full_response = ""
            async for chunk in stream_generator_math(response, session_id=session_id):
                full_response += chunk

            clean_text, code = code_extractor.extract_code(full_response)

            final_response = ""

            if code:
                result = sandbox.run(code)
                try:
                    sanitizer = LatexSanitizer()
                    result = sanitizer.process_result(result_str=result)
                except Exception as e:
                    logger.warning(f"LaTeX conversion failed: {e}")

                logger.info(f"Sandbox: {result}")

                final_response = clean_text.replace("[CODE BLOCK REMOVED]", f"Result: $ {result} $")
            else:

                final_response = full_response

            db_utils.save_message(session_id=session_id, role="astra", content=final_response)

            response_to_return = Response(content=final_response, media_type="text/plain")  
            response_to_return.headers["X-session-ID"] = session_id
            response_to_return.headers["showSteps"] = str(True)
            return response_to_return
        else:

            
            streaming_response =  StreamingResponse(
                stream_generator_other(response, session_id),
                media_type="text/plain",
            )

            streaming_response.headers["X-session-ID"] = session_id

            return streaming_response
        
    except Exception as e:
        logger.error(f"Message response: {e}")
        return {"ERROR": f"{e}"}
    
@router.get("/message-response")
async def handle_message_get():
    return {"error": "Use POST method"}


@router.post("/explain-steps")
async def handle_message(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt")

        response = generate_steps(prompt)
        return {"steps": str(response)}
    except Exception as e:
        logger.error(f"Steps generation: {e}")
        return {"steps": f"Error: {str(e)}"}

@router.post("/ocr-to-latex")
async def ocr_to_latex_endpoint(file: UploadFile = File(...)):
    model = LatexOCRModel()
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        latex = model.predict(tmp_path)
        os.unlink(tmp_path)
        return latex
    except Exception as e:
        logger.error(f"OCR error: {e}")
        return {"error": str(e), "status": "failed"}