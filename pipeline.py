from rich import print
from agents.agents import web_search_agent, web_reader_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str) -> dict:
    """
    Run the full multi-agent research pipeline for a given topic.

    Pipeline stages:
        1. Web Search Agent  — broad search for recent information.
        2. Web Reader Agent  — deep-scrapes the most relevant URL.
        3. Writer Chain      — synthesises findings into a structured report.
        4. Critic Chain      — peer-reviews the report and scores it.

    Args:
        topic (str): The research question or topic to investigate.

    Returns:
        dict: State dict containing search results, research report, and critic report.
    """