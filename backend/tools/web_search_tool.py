from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import ToolException
from dotenv import load_dotenv

load_dotenv()

def get_working_search_tool():
    try:
        tavily_tool = TavilySearchResults()
        # Do a test query
        tavily_tool.run("ping", max_results=1)
        print("✅ Using Tavily")
        return tavily_tool
    except Exception as e:
        print(f"⚠️ Tavily failed, switching to DuckDuckGo: {e}")
        return DuckDuckGoSearchRun()

web_search_tool = get_working_search_tool()
