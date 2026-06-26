from fastapi import APIRouter, Depends
from app.schemas.research import ResearchRequest, ResearchResponse
from app.services.research_service import ResearchService

router = APIRouter()

def get_research_service() -> ResearchService:
    return ResearchService()

@router.post("/", response_model=ResearchResponse)
async def perform_research(
    request: ResearchRequest,
    service: ResearchService = Depends(get_research_service)
):
    """
    Run the full multi-agent research pipeline for a given topic.
    Note: This is a synchronous operation and may take some time to complete.
    """
    return service.run_pipeline(topic=request.topic)
