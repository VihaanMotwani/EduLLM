from langchain_tavily import TavilySearch
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import ToolException
from dotenv import load_dotenv

load_dotenv()

def get_working_search_tool():
    try:
        tavily_tool = TavilySearch()
        # Do a test query
        tavily_tool.run("ping", max_results=1)
        print("✅ Using Tavily")
        return tavily_tool
    except Exception as e:
        print(f"⚠️ Tavily failed, switching to DuckDuckGo: {e}")
        ddg_tool = DuckDuckGoSearchRun()
        return ddg_tool

web_search_tool = get_working_search_tool()
