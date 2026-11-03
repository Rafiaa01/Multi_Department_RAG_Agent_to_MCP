from fastapi import APIRouter

from src.controllers.session_controllers import (
    handle_create_session,
    handle_delete_session,
    handle_get_all_sessions,
    handle_get_session,
)
from src.schemas.chat_schemas import SessionResponse

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("", response_model=SessionResponse)
def create_new_session():
    return handle_create_session()


@router.get("/{session_id}", response_model=SessionResponse)
def get_existing_session(session_id: str):
    return handle_get_session(session_id)


@router.delete("/{session_id}")
def remove_session(session_id: str):
    return handle_delete_session(session_id)
 
@router.get("")
def get_all_existing_sessions():
    return handle_get_all_sessions()