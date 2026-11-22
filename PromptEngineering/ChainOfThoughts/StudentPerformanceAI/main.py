from fastapi import FastAPI
from services.llm_service import analyze_student_performance 
from models.student_model import StudentPerformanceResponse,StudentPerformanceAnalysis,StudentPerformanceRequest

app=FastAPI(title="Student Performance AI")

@app.get("/")
def home():
    return {
        "message":"Student Performace AI"
    }

@app.post("/api/v1/analyze-student",response_model=StudentPerformanceResponse)
def analyze_student(request:StudentPerformanceRequest):
    return analyze_student_performance(request)
