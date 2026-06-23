from langchain.tools import tool
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from rich import print
import os

load_dotenv()


@tool
def web_search(query: str) -> str:
    """
    Search the web for real-time information using Tavily.

    Use this tool when you need up-to-date information that may not be
    in your training data, such as recent news, current events, or
    live data.

    Args:
        query (str): The search query string to look up on the web.

    Returns:
        str: A string containing the search results from Tavily,
             including relevant snippets and sources.
    """
    tavily = TavilySearch()
    response = tavily.invoke({"query": query})
    doc = []
    for r in response.get("results", []):
        doc.append(
            {
                "url": r.get("url", ""),
                "title": r.get("title", "No Title"),
                "content": r.get("content", ""),
                "score": r.get("score", 0.0),
                "source": "tavily_web_search",
            }
        )

    return doc


print(web_search.invoke("Pakistan mediation role in IRAN-US war?"))
