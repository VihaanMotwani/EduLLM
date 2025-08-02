from langchain_openai import ChatOpenAI
from typing import Literal
from graph.schemas import RouteDecision, RagJudge, AgentState
import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM instances with structured output where needed ───────────────

router_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)\
             .with_structured_output(RouteDecision)
judge_llm  = ChatOpenAI(model="gpt-4o-mini", temperature=0)\
             .with_structured_output(RagJudge)
answer_llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# ── Routing helpers ─────────────────────────────────────────────────
def from_router(st: AgentState) -> Literal["rag", "answer", "end"]:
    return st["route"]

def after_rag(st: AgentState) -> Literal["answer", "web"]:
    return st["route"]

def after_web(_) -> Literal["answer"]:
    return "answer"