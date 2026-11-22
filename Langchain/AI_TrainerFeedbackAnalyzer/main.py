from fastapi import FastAPI
from services.llm_service import analyze_feedback
from models.trainer_feedback_model import TrainerFeedbackRequest,TrainerFeedbackResponse

app=FastAPI(title="AI Trainer Feedback Analyzer")

@app.get("/home")
def home():
    return "Home"

@app.post("/api/v1/analyze_feedback",response_model=TrainerFeedbackResponse)
def analyze(request:TrainerFeedbackRequest):
    response=analyze_feedback(request)
    return response

