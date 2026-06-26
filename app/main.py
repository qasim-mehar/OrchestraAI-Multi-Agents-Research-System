from fastapi import FastAPI
from app.api.router import api_router
from app.core.exceptions import ResearchPipelineError, research_pipeline_exception_handler
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="OrchestraAI Backend",
    description="A multi-agent research system API.",
    version="0.1.0"
)

# Exception Handlers
app.add_exception_handler(ResearchPipelineError, research_pipeline_exception_handler)

# Routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}
