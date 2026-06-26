from pydantic import BaseModel, Field

class ResearchRequest(BaseModel):
    topic: str = Field(..., description="The research question or topic to investigate.")

class ResearchResponse(BaseModel):
    basic_results: str = Field(..., description="Results from the initial broad web search.")
    advanced_research_results: str = Field(..., description="Detailed scraped content from the most relevant source.")
    research_report: str = Field(..., description="The synthesized research report.")
    critic_report: str = Field(..., description="The peer-review critique of the research report.")
