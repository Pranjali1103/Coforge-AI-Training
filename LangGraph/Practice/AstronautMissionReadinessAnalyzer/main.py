from fastapi import FastAPI
from models.ai_model import AstronautRequest,AstronautResponse
from workflow.astronaut_workflow import workflow_graph
from services.llm_service import analyze_astronaut_mission

app=FastAPI(title="Hey Astronaut here")

@app.get("/home")
def home():
    return "home"


@app.post("/api/v1/analyze_astronaut",response_model=AstronautResponse)
def analyze_astronaut(request:AstronautRequest):
    result=workflow_graph.invoke({
        "astronaut_id":request.astronaut_id,
        "astronaut_name":request.astronaut_name,
        "age":request.age,
        "training_hours":request.training_hours,
        "medical_clearance":request.medical_clearance,
        "previous_missions":request.previous_missions
    })
    return AstronautResponse(
        astronaut_id=result["astronaut_id"],
        astronaut_name=result["astronaut_name"],
        mission_status=result["mission_status"],
        assigned_mission=result["assigned_mission"],
        reason=result["reason"]
    )


    # print("hi")
    # result=analyze_astronaut_mission(request)
    # return result 