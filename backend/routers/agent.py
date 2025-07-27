from fastapi import APIRouter
from pydantic import BaseModel
from services.agent_service import create_agent
from langchain_core.messages import HumanMessage

class AgentRequest(BaseModel):
    query: str

router = APIRouter()
agent_executor = create_agent()

@router.post("/invoke")
async def invoke_agent(request: AgentRequest):
    """
    Invokes the ReAct agent and streams the response, printing internal steps.
    """
    inputs = {"messages": [HumanMessage(content=request.query)]}
    response_content = ""

    print("\n--- New Request ---")
    async for event in agent_executor.astream_events(inputs, version="v1"):
        kind = event["event"]
        # Print the event to the console
        print(f"EVENT: {kind}")

        # If the event is the start of a tool, print its input
        if kind == "on_tool_start":
            print(f'  - Tool: {event["name"]}')
            print(f'  - Input: {event["data"]["input"]}')

        # If the event is the end of a tool, print its output
        if kind == "on_tool_end":
            output_content = event["data"]["output"].content
            print(f'  - Output: {output_content[:150]}...') # Print first 150 chars

        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                response_content += content

    print("--- Request End ---\n")
    return {"response": response_content}