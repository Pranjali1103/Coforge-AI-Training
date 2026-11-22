from fastapi import FastAPI
from models.ai_model import EmployeeFeedbackResponse,EmployeeFeedbackRequest
from services.llm_service import generate_employee_performance_feedback


app=FastAPI(title="Employee Performance Feedback AI")

@app.get("/home")
def home():
    return{
        "message":"Employee Performance Feedback AI is working"
    }


@app.post("/api/v1/analyze-employee",response_model=EmployeeFeedbackResponse)
def analyse_employee_performaance(request:EmployeeFeedbackRequest):
    response=generate_employee_performance_feedback(request)
    return response