from fastapi import Request
from fastapi.responses import JSONResponse

class ResearchPipelineError(Exception):
    """Base exception for research pipeline errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

async def research_pipeline_exception_handler(request: Request, exc: ResearchPipelineError):
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message, "type": "research_pipeline_error"},
    )
