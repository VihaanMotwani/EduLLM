from typing import List, Literal, Optional, TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage

class AgentState(TypedDict, total=False):
    messages: List[BaseMessage]
    route:    Literal["rag", "answer", "end"]
    rag:      str
    web:      str

class RouteDecision(BaseModel):
    route: Literal["rag", "answer", "end"]
    reply: Optional[str] = Field(None, description="Filled only when route == 'end'")

class RagJudge(BaseModel):
    sufficient: bool
