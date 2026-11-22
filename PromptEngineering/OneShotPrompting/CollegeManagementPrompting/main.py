from fastapi import FastAPI
from services.llm_service import analyze_student_profile
from models.ai_model import StudentResponse,StudentAnalysis,StudentRequest

app=FastAPI(title="Student Profile Analyzer")

@app.get("/home")
def Home():
    return{
        "message":"student profile analyzer"
    }

@app.post("/api/v1/profile-analyzer",response_model=StudentResponse)
def analyze_profile(request:StudentRequest)->StudentResponse:
     response=analyze_student_profile(request)
     return response