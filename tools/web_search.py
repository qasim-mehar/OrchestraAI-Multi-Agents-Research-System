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
        str: A formatted string containing the search results from Tavily,
             including relevant snippets and sources.
    """
    tavily = TavilySearch()
    response = tavily.invoke({"query": query})

    formatted_results = []

    for search_result in response.get("results", []):
        url = search_result.get("url", "No URL")
        title = search_result.get("title", "No Title")
        content = search_result.get("content", "No content available")
        relevance_score = search_result.get("score", 0.0)

        result_block = (
            f"Source: {title}\n"
            f"URL: {url}\n"
            f"Relevance: {relevance_score:.4f}\n"
            f"Content: {content}"
        )

        formatted_results.append(result_block)

    return "\n\n----\n\n".join(formatted_results)
