from fastapi import FastAPI, UploadFile, Form, Request, File
from typing import Annotated, Optional
from fastapi.responses import FileResponse, StreamingResponse, Response, PlainTextResponse
from intent import intent_classifier
from intent import task_extractor
from fastapi.staticfiles import StaticFiles
import shutil
from core import ollama_call
from pdf_module.chunker import chunk_text
from pdf_module.parser import extract_text
from pdf_module.memory import store_chunks, get_chunks
from pdf_module.ask_llm import ask_llm
import json
from tools import sandbox, code_extractor
from memory import db_utils
from contextlib import asynccontextmanager
import sympy as sp
import re
import tempfile
import os
from ocr_module import LatexOCRModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_utils.init_db()
    print("DB INITIALISED")
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static",html = True), name="static")

@app.get("/")
def test_form():
    return FileResponse("static/index.html")

@app.get("/test-form")
def test_form():
    return FileResponse("static/test.html")


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile):
    with open("data/temp.pdf", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text("data/temp.pdf")
    chunks = chunk_text(text)

    store_chunks(chunks)

    return {
        "message": "PDF processed",
        "num_chunks": len(chunks)
    }

@app.get("/ask_llm")
def _ask_pdf():
    answer = ask_llm()
    return {
        "answer": answer
    }


@app.post("/submit")
async def handle_form(
    username: Annotated[str, Form()], 
    email: Annotated[str, Form()]
):
    return {"message": f"Received data for {username}", "status": "success"}


@app.post("/message-response")
async def handle_message(
    message: Annotated[str, Form()],
    subject: Annotated[str, Form()],
    image: Optional[UploadFile] = File(None),
    pdf: Optional[UploadFile] = File(None),
    session_id: Optional[str] = Form(None)
    ):

    if not session_id:
        session_id = db_utils.create_session()
    else:
        print("RECEIVED SESSION ID", session_id)

    db_utils.save_message(session_id=session_id, role="user", content=message)

    history = db_utils.get_recent_messages(session_id=session_id, limit=10)

    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])

    int_conf = intent_classifier.classify_intent(message)

    print(f"CLASSIFICATION SUCCESSFULL, intent: {int_conf['intent']}")

    task_topic = ""
    if int_conf["intent"] == "chat":
        task_topic = {"task": "conversation", "topic": message}
    else:
        task_topic = task_extractor.extract_best(message)

    print(f"TASK TOPIC: {task_topic}")

    try:


        response = ollama_call.message_response(message=message, intent=int_conf["intent"], confidence=int_conf["confidence"], task=task_topic["task"], topic=task_topic["topic"], context=context)

        
        
        full_response = ""

        if int_conf["intent"] == "math_solve":

            full_response = ""
            async for chunk in stream_generator_math(response, session_id=session_id):
                full_response += chunk

            clean_text, code = code_extractor.extract_code(full_response)

            final_response = ""

            if code:
                result = sandbox.run(code)
                result = sp.latex(sp.sympify(result))
                result = re.sub(r'\\log', r'\\operatorname{ln}', result)
                print(f"SANDBOX RESULT: {result}")

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
        print(f"ERROR: {e}")
        return {"ERROR": f"{e}"}
    
async def stream_generator_math(response, session_id):

    full_response=""

    for line in response.iter_lines():
        
        
        if line:
            line_str = line.decode('utf-8')
            try:
                data = json.loads(line_str)
                token = data.get("response", "")


                done = data.get("done", False)

                full_response += token

                yield token
            except Exception as e:


                yield line_str
                
async def stream_generator_other(response, session_id):

    full_response=""

    for line in response.iter_lines():
        
        
        if line:
            line_str = line.decode('utf-8')
            try:
                data = json.loads(line_str)
                token = data.get("response", "")


                done = data.get("done", False)

                full_response += token

                if done and session_id:
                    db_utils.save_message(session_id=session_id, role="astra", content=full_response)

                yield token
            except Exception as e:
                print(f"ERROR IN STREAM GEN: {e}")  

                yield line_str
                
@app.get("/message-response")
async def handle_message_get():
    return {"error": "Use POST method"}


@app.post("/explain-steps")
async def handle_message(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt")

        response = ollama_call.explain_steps(prompt)
        return {"steps": str(response)}
    except Exception as e:
        print(f"ERROR: {e}")
        return {"steps": f"Error: {str(e)}"}
    

@app.post("/new-session")
async def new_session():
    new_session_id = db_utils.create_session()
    return {"session_id": new_session_id}

@app.get("/get-sessions")
async def get_sessions():
    sessions = db_utils.get_all_sessions()
    return {"sessions": sessions}

@app.get("/session/{session_id}/messages")
async def get_session_messages(session_id: str):
    messages = db_utils.get_recent_messages(session_id)
    print("MESSAGES-MAIN: ", messages)
    return {"messages": messages}
@app.get("/session/{session_id}/messages")

@app.get("/session/{session_id}/delete")
async def delete_session(session_id: str):

    try:
        db_utils.delete_session(session_id=session_id)
        return {"response": "SUCCESSFUL"}
    except:
        return {"response": "UNSUCCESSFUL"}
    

@app.post("/ocr-to-latex")
async def ocr_to_latex(file: UploadFile = File(...)):
    model = LatexOCRModel()
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        latex = model.predict(tmp_path)
        os.unlink(tmp_path)
        
        return PlainTextResponse(latex)
    except Exception as e:
        return {"error": str(e), "status": "failed"}