import os
from dotenv import load_dotenv 
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

load_dotenv()

# 1. Define the state for our graph
#    This will be the "memory" of our agent.
class AgentState(TypedDict):
    # The 'messages' key will hold the list of messages in the conversation.
    messages: Annotated[list, operator.add]

# 2. Define the main agent node
#    This function will be called every time the agent needs to act.
def call_model(state):
    messages = state['messages']
    model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # Call the model with the current messages
    response = model.invoke(messages)
    # Return the new state with the model's response appended to the messages
    return {"messages": [response]}

# 3. Define the graph
def create_agent_graph():
    # Initialize the state graph
    graph = StateGraph(AgentState)
    # Add the main node
    graph.add_node("llm", call_model)
    # Set the entry point for the graph
    graph.set_entry_point("llm")
    # Add a final edge to the END node
    graph.add_edge("llm", END)
    # Compile the graph into a runnable object
    return graph.compile()