from langchain_core.tools import tool
from services.rag_service import get_raptor_retriever

retriever = get_raptor_retriever()

@tool
def search_knowledge_base(query: str):
    """
    Looks up relevant documents from the EduLLM knowledge base to answer a user's question
    about AI, Machine Learning, or related topics.
    """
    # The retriever returns a list of Document objects. We need to format them.
    retrieved_docs = retriever.retrieve(query)

    if not retrieved_docs:
        print("--- RAG Tool: No info found. ---")
        return "No relevant information was found in the knowledge base for this query."

    # We'll format the output to be a clean string for the LLM.
    formatted_context = "\n\n".join([doc.text for doc in retrieved_docs])
    if not formatted_context:
        return "No relevant information found in the knowledge base."
    return f"Retrieved context:\n\n{formatted_context}"