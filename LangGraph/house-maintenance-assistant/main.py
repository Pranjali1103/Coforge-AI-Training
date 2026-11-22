from fastapi import FastAPI
from models.maintenance_model import MaintenanceRequest,MaintenanceResponse

from workflow.maintenance_workflow import MaintenanceState
from workflow.maintenance_workflow import workflow_graph

app=FastAPI(title="House-Maintenance-Assistant")


@app.get("/home")
def home():
    return "home"

@app.post("/api/v1/maintenance_question",response_model=MaintenanceResponse)
def maintenance_question(request:MaintenanceRequest):
    result=workflow_graph.invoke(
    {
        "question":request.question
    }
    )
    return MaintenanceResponse(
    question=request.question,
    answer=result["answer"]

)
