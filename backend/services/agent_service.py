from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from .rag_service import get_raptor_retriever

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
        If the tool returns a message saying 'No relevant information was found', 
        you MUST stop and answer using your own knowledge. If you do not know the answer either, 
        you must inform the user that you couldn't find the required information
        and point them towards other resources. 
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