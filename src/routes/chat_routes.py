import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from src.controllers.chat_controllers import handle_chat
from src.schemas.chat_schemas import ChatRequest, ChatResponse

router = APIRouter()

HISTORY_FILE = Path(__file__).resolve().parents[1] / "data" / "chat_history.json"


def load_history():
    if not HISTORY_FILE.exists():
        return {}

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_history(history):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)


@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        return handle_chat(request)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request."
        ) from exc