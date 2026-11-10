
from src.schemas.chat_schemas import ChatRequest, ChatResponse
from src.services.chat import chat_with_history

agent = None


def set_agent(department_agent):
    global agent
    agent = department_agent


async def handle_chat(request: ChatRequest) -> ChatResponse:
    if agent is None:
        raise RuntimeError("Agent has not been initialized")

    result = await chat_with_history(agent, request)

    return ChatResponse(
        answer=result["answer"],
        history=result["history"],
    )
