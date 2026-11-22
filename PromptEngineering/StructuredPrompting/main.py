from fastapi import FastAPI
from services.llm_service import analyze_learner_performance
from models.ai_model import (
    LearnerRequest,
    LearnerAnalysis,
    LearnerResponse
)

app=FastAPI(title="Training Performance AI")


@app.get("/home")
def home():
    return "Home"


@app.post("/api/v1/analyze_performance",response_model=LearnerResponse)
def analyze_performance(request:LearnerRequest)->LearnerResponse:
    response=analyze_learner_performance(request)
    return response 

   

