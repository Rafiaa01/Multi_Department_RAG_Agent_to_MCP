from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.controllers.chat_controllers import set_agent
from src.routes.chat_routes import router as chat_router
from src.routes.session_routes import router as session_router
from src.services.agent_services import initialize_agent


@asynccontextmanager
async def lifespan(application: FastAPI):

    agent = initialize_agent()
    set_agent(agent)

    yield


application = FastAPI(
    title="Multi-Department RAG Agent",
    description="An AI assistant for HR, IT, and Finance documents.",
    version="1.0.0",
    lifespan=lifespan,
)

application.include_router(chat_router)
application.include_router(session_router)
