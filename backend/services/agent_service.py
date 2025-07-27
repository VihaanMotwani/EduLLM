from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate

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
    Creates and returns a compiled ReAct agent graph with a system prompt.
    """
    # Define the system prompt
    system_prompt = (
        """
        You are EduLLM, a specialized AI and Machine Learning tutor.
        Your goal is to help users learn complex topics by providing clear,
        concise, and accurate explanations. When a user asks a question,
        first decide if you can answer it from your general knowledge or if you
        need to use the search_knowledge_base tool to consult the provided documents.
        Be friendly, encouraging, and always aim to simplify difficult concepts.
        """
    )

    # Create a prompt template that includes the system message
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    
    model = ChatOpenAI(model="gpt-4o", temperature=0)

    # Bind the prompt to the model and then the tools
    agent_with_prompt = prompt | model.bind_tools(tools)

    # Create the agent executor graph with the new model-prompt combination
    agent_executor = create_react_agent(agent_with_prompt, tools)
    
    return agent_executor