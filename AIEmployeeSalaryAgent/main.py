from fastapi import FastAPI
from services.llm_service import calculate_employee_salary
from models.ai_model import SalaryResponse,SalaryRequest

app=FastAPI(title="AI Employee Salary Agent")

@app.get("/home")
def home():
    return "Home"

@app.post("/api/v1/employee_salary",response_model=SalaryResponse)
def calculate_salary(request:SalaryRequest)->SalaryResponse:
    response=calculate_employee_salary(request)
    return response

