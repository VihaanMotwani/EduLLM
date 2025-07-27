from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# Import our RAPTOR retriever function
from .rag_service import get_raptor_retriever

# 1. Initialize the retriever when the service starts
retriever = get_raptor_retriever()

# 2. Use the @tool decorator to create a tool from our retriever
@tool
def search_knowledge_base(query: str):
    """
    Looks up relevant documents from the EduLLM knowledge base to answer a user's question
    about AI, Machine Learning, or related topics.
    """
    # The retriever returns a list of Document objects. We need to format them.
    retrieved_docs = retriever.retrieve(query)
    # We'll format the output to be a clean string for the LLM.
    formatted_context = "\n\n".join([doc.text for doc in retrieved_docs])
    if not formatted_context:
        return "No relevant information found in the knowledge base."
    return f"Retrieved context:\n\n{formatted_context}"

# 3. Define the list of tools the agent can use
tools = [search_knowledge_base]

# 4. Create the agent using the high-level constructor
def create_agent():
    """
    Creates and returns a compiled ReAct agent graph.
    """
    # Define the language model
    # Note: GPT-4o is recommended for better tool-using capabilities
    model = ChatOpenAI(model="gpt-4o", temperature=0)

    # Create the agent executor graph
    agent_executor = create_react_agent(model, tools)
    
    return agent_executor