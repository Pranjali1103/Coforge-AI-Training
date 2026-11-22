from fastapi import APIRouter
from models.request_model import LearnerProgressRequest
from models.response_model import LearnerProgressResponse
from services.ai_service import analyze_progress

router=APIRouter(
    prefix="/api/training",
    tags=["Training Progress"]
)

@router.get("/health")
def getHealth():
    return { "status":"healthy"}

@router.post("/analyze-progress",response_model=LearnerProgressResponse)
def analyze_learner_progress(request:LearnerProgressRequest):
    return analyze_progress(request)