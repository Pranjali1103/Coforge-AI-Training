from fastapi import FastAPI
from models.ai_model import StudentAssignmentResponse,StudentAssignmentRequest
from services.llm_service import student_assessment_evaluation


app=FastAPI(title="Student Assignment Evaluation AI")

@app.get("/home")
def home():
    return{
        "message":"Student Assignment Evaluation AI is working"
    }


@app.post("/api/v1/evaluate-assignment",response_model=StudentAssignmentResponse)
def evaluate_assignment(request:StudentAssignmentRequest):
    response=student_assessment_evaluation(request)
    return response