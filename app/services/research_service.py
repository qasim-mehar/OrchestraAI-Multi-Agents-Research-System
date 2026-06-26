import logging
from app.infrastructure.agents import web_search_agent, web_reader_agent, writer_chain, critic_chain
from app.schemas.research import ResearchResponse
from app.core.exceptions import ResearchPipelineError

logger = logging.getLogger(__name__)

class ResearchService:
    @staticmethod
    def run_pipeline(topic: str) -> ResearchResponse:
        """
        Run the full multi-agent research pipeline for a given topic.

        Args:
            topic (str): The research question or topic to investigate.

        Returns:
            ResearchResponse: The response containing search results, research report, and critic report.
        """
        try:
            state = {}

            logger.info(f"Stage 1: Searching the web for '{topic}'...")
            search_agent = web_search_agent()
            
            basic_search_result = search_agent.invoke({
                "messages": [("human", f"Find recent, reliable and detailed information about: {topic}")]
            })

            state["basic_results"] = basic_search_result["messages"][-1].content
            logger.info("Stage 1 complete.")

            logger.info("Stage 2: Scraping the most relevant source...")
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
            logger.info("Stage 2 complete.")

            logger.info("Stage 3: Writing the research report...")
            combined_research = (
                f"## BASIC SEARCH RESULTS\n{state['basic_results']}\n\n"
                f"## DETAILED SCRAPED CONTENT\n{state['advanced_research_results']}"
            )

            state["research_report"] = writer_chain.invoke({
                "topic": topic,
                "research": combined_research,
            })
            logger.info("Stage 3 complete.")

            logger.info("Stage 4: Running peer review...")
            state["critic_report"] = critic_chain.invoke({
                "topic": topic,
                "research_report": state["research_report"],
            })
            logger.info("Stage 4 complete.")

            return ResearchResponse(**state)

        except Exception as e:
            logger.error(f"Error during research pipeline: {str(e)}", exc_info=True)
            raise ResearchPipelineError(f"Failed to complete research pipeline: {str(e)}")
