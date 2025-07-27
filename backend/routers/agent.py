from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List
from services.agent_service import create_agent
from langchain_core.messages import HumanMessage, AIMessage

# Define the structure for a single message in the history
class ChatMessage(BaseModel):
    sender: str
    text: str

# The request will now contain the entire message history
class AgentRequest(BaseModel):
    messages: List[ChatMessage]

router = APIRouter()
agent_executor = create_agent()

@router.post("/invoke")
async def invoke_agent(request: AgentRequest):
    """
    Invokes the ReAct agent with the entire conversation history.
    """
    # Convert our simple ChatMessage objects into LangChain's message objects
    history = []
    for msg in request.messages:
        if msg.sender == 'user':
            history.append(HumanMessage(content=msg.text))
        elif msg.sender == 'ai':
            history.append(AIMessage(content=msg.text))

    inputs = {"messages": history}
    response_content = ""

    # The streaming logic remains the same
    print("\n--- New Request ---")
    async for event in agent_executor.astream_events(inputs, version="v1"):
        kind = event["event"]
        print(f"EVENT: {kind}")

        if kind == "on_tool_start":
            print(f'  - Tool: {event["name"]}')
            print(f'  - Input: {event["data"]["input"]}')

        if kind == "on_tool_end":
            output_content = event["data"]["output"].content
            print(f'  - Output: {output_content[:150]}...')

        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                response_content += content

    print("--- Request End ---\n")
    return {"response": response_content}