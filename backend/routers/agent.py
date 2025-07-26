from fastapi import APIRouter
from pydantic import BaseModel
from services.agent_service import create_agent_graph
from langchain_core.messages import HumanMessage

# Define the request model for our endpoint
class AgentRequest(BaseModel):
    query: str

router = APIRouter()
agent_graph = create_agent_graph()

@router.post("/invoke")
def invoke_agent(request: AgentRequest):
    # Format the input for the LangGraph agent
    inputs = {"messages": [HumanMessage(content=request.query)]}
    # Run the agent
    result = agent_graph.invoke(inputs)
    # Extract the last message (the AI's response)
    response = result['messages'][-1].content
    return {"response": response}