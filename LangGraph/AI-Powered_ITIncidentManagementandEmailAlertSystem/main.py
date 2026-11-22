from fastapi import FastAPI
from models.incident_model import (
    IncidentRequest,
    IncidentResponse
)
from workflow.incident_workflow import IncidentState
from workflow.incident_workflow import workflow_graph

app=FastAPI(title="AI-Powered_ITIncidentManagement")

@app.get("/home")
def home():
    return "home"

@app.post("/api/v1/analyze_incident",response_model=IncidentResponse)
def analyze_incident(request:IncidentRequest):
    result=workflow_graph.invoke({
        "employee_id":request.employee_id,
        "employee_name": request.employee_name,
        "department": request.department,
        "issue": request.issue
    })
    return IncidentResponse(
        employee_id=result["employee_id"],
        employee_name=result["employee_name"],
        category=result["category"],
        priority=result["priority"],
        summary=result["summary"],
        suggested_resolution=result["suggested_resolution"],
        escalation_required=result["escalation_required"],
        email_sent=result["email_sent"],
        status=result["status"]
    )