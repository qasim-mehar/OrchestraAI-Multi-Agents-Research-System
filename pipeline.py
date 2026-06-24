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
    state = {}

    #  Broad Web Search
    print(f"\n[bold cyan] Stage 1: Searching the web for '{topic}'...[/bold cyan]")

    search_agent = web_search_agent()


    basic_search_result = search_agent.invoke({
        "messages": [("human", f"Find recent, reliable and detailed information about: {topic}")]
    })

    state["basic_results"] = basic_search_result["messages"][-1].content
    print("[green] Stage 1 complete.[/green]")

    #  Deep Web Scrape
    print("\n[bold cyan] Stage 2: Scraping the most relevant source...[/bold cyan]")

    web_reader = web_reader_agent()


    search_snippet = state["basic_results"][:800]

    advanced_research_result = web_reader.invoke({
        "messages": [("human",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{search_snippet}"
        )]
    })

    state["advanced_research_results"] = advanced_research_result["messages"][-1].content
    print("[green] Stage 2 complete.[/green]")

    # Write Report
    print("\n[bold cyan]  Stage 3: Writing the research report...[/bold cyan]")

    combined_research = (
        f"## BASIC SEARCH RESULTS\n{state['basic_results']}\n\n"
        f"## DETAILED SCRAPED CONTENT\n{state['advanced_research_results']}"
    )


    state["research_report"] = writer_chain.invoke({
        "topic": topic,
        "research": combined_research,
    })
    print("[green] Stage 3 complete.[/green]")

    #  Critic Review
    print("\n[bold cyan] Stage 4: Running peer review...[/bold cyan]")

    state["critic_report"] = critic_chain.invoke({
        "topic": topic,
        "research_report": state["research_report"],
    })
    print("[green] Stage 4 complete.[/green]")

    return state


def display_results(state: dict) -> None:
    """Pretty-print the final pipeline output."""
    print("\n" + "=" * 70)
    print("[bold yellow] RESEARCH REPORT[/bold yellow]")
    print("=" * 70)
    print(state["research_report"])

    print("\n" + "=" * 70)
    print("[bold magenta] CRITIC REVIEW[/bold magenta]")
    print("=" * 70)
    print(state["critic_report"])
