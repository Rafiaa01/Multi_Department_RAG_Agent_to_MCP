from fastapi import HTTPException

from src.services.session_management import (
    create_session,
    delete_session,
    get_all_sessions,
    get_session,
)


def handle_create_session():
    return create_session()


def handle_get_session(session_id: str):
    session = get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    return {"session_id": session_id, "history": session}


def handle_delete_session(session_id: str):
    deleted = delete_session(session_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    return {"message": "Session deleted successfully"}


def handle_get_all_sessions():
    return get_all_sessions()
