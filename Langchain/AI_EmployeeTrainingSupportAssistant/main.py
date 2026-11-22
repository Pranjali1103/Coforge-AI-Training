from fastapi import FastAPI, HTTPException

from models.employee_model import (
    TrainingRequest,
    TrainingResponse
)

from services.llm_service import analyze_training

app = FastAPI(title="AI Employee Training Support Assistant")

@app.post(
    "/training/ask",
    response_model=TrainingResponse
)
def ask_training_question(request: TrainingRequest):
    return analyze_training(request)