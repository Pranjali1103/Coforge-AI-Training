from fastapi import APIRouter
from models.training_model import TrainingRequest,TrainingResponse
from services.training_service import analyze_training_question

router=APIRouter(
    prefix="/api/training",
    tags=["Training Assistant"]
)

@router.get("/health")
def health():
    return{
        "status":"healthy"
    }

@router.get("/role")
def getRole(response:TrainingResponse):
    return {
        "role":"Corporate IT Trainer",
        "supported_topics": [
            "Python",
            "Pandas",
            "NumPy",
            "MySQL",
            "SQLAlchemy",
            "FastAPI",
            "Data Engineering",
            "ETL",
            "Generative AI",
            "LLMs",
            "Prompt Engineering"
        ]  
    }



@router.post("/ask",response_model=TrainingResponse)
def ask_question(request:TrainingRequest)->TrainingResponse:
    response=analyze_training_question(request)
    return response
