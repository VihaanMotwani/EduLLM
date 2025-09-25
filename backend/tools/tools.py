from langchain_tavily import TavilySearch
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

from rag.raptor_service import get_raptor_retriever

tavily = TavilySearch(max_results=3, topic="general")

raptor_retriever = get_raptor_retriever()

@tool
def web_search_tool(query: str) -> str:
    """Up-to-date web info via Tavily"""
    try:
        result = tavily.invoke({"query": query})

        # Extract and format the results from Tavily response
        if isinstance(result, dict) and 'results' in result:
            formatted_results = []
            for item in result['results']:
                title = item.get('title', 'No title')
                content = item.get('content', 'No content')
                url = item.get('url', '')
                formatted_results.append(f"Title: {title}\nContent: {content}\nURL: {url}")

            return "\n\n".join(formatted_results) if formatted_results else "No results found"
        else:
            return str(result)
    except Exception as e:
        return f"WEB_ERROR::{e}"

@tool
def rag_search_tool(query: str) -> str:
    """Top-3 chunks from KB using RAPTOR (empty string if none)"""
    try:
        # The LlamaIndex retriever uses the .retrieve() method
        nodes = raptor_retriever.retrieve(query)
        # Format the output nodes into a single string for the context
        return "\n\n".join(node.get_content() for node in nodes) if nodes else ""
    except Exception as e:
        return f"RAG_ERROR::{e}"