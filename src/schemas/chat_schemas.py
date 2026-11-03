
from typing import Literal

from pydantic import BaseModel, Field


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    answer: str
    history: list[HistoryMessage] = Field(default_factory=list)


class SessionResponse(BaseModel):
    session_id: str
    history: list[HistoryMessage] = Field(default_factory=list)







