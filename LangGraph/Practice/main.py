from fastapi import FastAPI
from models.training_model import (
    TrainerRequest,
    TrainerResponse
)
from workflow.training_workflow import workflow_graph
from services.llm_service import analyze_training_feedback

app=FastAPI(title="Training Feedback")

@app.get("/home")
def Home():
    return{
        "status":"Hello I am the best"
    }


@app.post("/api/v1/analyze-feeback",response_model=TrainerResponse)
def analyze_feedback(request:TrainerRequest):
    result=workflow_graph.invoke({
        "trainer_name":request.trainer_name,
        "learner_name":request.learner_name,
        "trainer_rating":request.trainer_rating,
        "trainer_feedback":request.trainer_feedback,
        "trainer_topic":request.trainer_topic
    })
    return TrainerResponse(
        trainer_name=result["trainer_name"],
        sentiments=result["sentiments"],
        performance_level=result["performance_level"],
        strengths=result["strengths"],
        improvement_areas=result["improvement_areas"],
        overall_summary=result["overall_summary"],
        action_taken=result["action_taken"]
    )

    # without graph

    # result=analyze_training_feedback(request)
    # return result
