from fastapi import APIRouter
from memory import db_utils

router = APIRouter()


@router.post("/new-session")
async def new_session():
    new_session_id = db_utils.create_session()
    return {"session_id": new_session_id}

@router.get("/get-sessions")
async def get_sessions():
    sessions = db_utils.get_all_sessions()
    return {"sessions": sessions}

@router.get("/session/{session_id}/messages")
async def get_session_messages(session_id: str):
    messages = db_utils.get_recent_messages(session_id)
    return {"messages": messages}

@router.get("/session/{session_id}/delete")
async def delete_session(session_id: str):

    try:
        db_utils.delete_session(session_id=session_id)
        return {"response": "SUCCESSFUL"}
    except:
        return {"response": "UNSUCCESSFUL"}