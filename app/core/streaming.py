import json
from memory import db_utils
from core.logging import setup_logger


logger = setup_logger(__name__)

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
                    logger.info("done")
                    db_utils.save_message(session_id=session_id, role="astra", content=full_response)

                yield token
            except Exception as e:
                logger.error(f"Stream generator: {e}")  

                yield line_str