import json
import uuid
from pathlib import Path

HISTORY_FILE = Path(__file__).resolve().parents[1] / "data" / "chat_history.json"


def load_history():
    if not HISTORY_FILE.exists():
        return {}

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_history(sessions):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(sessions, file, indent=4, ensure_ascii=False)


def create_session():
    sessions = load_history()

    session_id = str(uuid.uuid4())
    sessions[session_id] = []

    save_history(sessions)

    return {"session_id": session_id, "history": []}


def get_session(session_id):
    sessions = load_history()
    return sessions.get(session_id)


def get_or_create_session(session_id):
    sessions = load_history()
    return sessions.get(session_id, [])


def update_session(session_id, history):
    sessions = load_history()
    sessions[session_id] = history
    save_history(sessions)


def delete_session(session_id):
    sessions = load_history()

    if session_id not in sessions:
        return False

    del sessions[session_id]
    save_history(sessions)

    return True


def get_all_sessions():
    sessions = load_history()

    return [
        {"session_id": session_id, "history": history}
        for session_id, history in sessions.items()
    ]
