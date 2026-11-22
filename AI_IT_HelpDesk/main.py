from fastapi import FastAPI,HTTPException
from models.helpdesk_model import HelpdeskRequest,HelpdeskResponse
from services.llm_service import process_helpdesk_request

app=FastAPI(
    title="Coforge AI IT Helpdesk"
    )




@app.get("/")
def home():
    return{
        "message":"AI IT Helpdesk"
    }



@app.post("/analyze",response_model=HelpdeskResponse)
def analyze_employee_issue(request:HelpdeskRequest):
        result=process_helpdesk_request(request)
        return result
    

# @app.post("/analyze",response_model=HelpdeskResponse)
# def analyze_employee_issue(request:HelpdeskRequest):
#     try:
#         result=process_helpdesk_request(request)
#         return result
#     except Exception:
#         # Do not expose API keys or internal errors
#         raise HTTPException(status_code=500,detail="Unable to process IT request")

























# from fastapi import FastAPI
# from services.llm_service import analyze_trainer_feedback
# from models.training_model import TrainerRequest,TrainerResponse
# from  workflow.training_workflow import TrainingFeedbackState
# from workflow.training_workflow import analyze_training_feedback_node
# from workflow.training_workflow import workflow_graph

# app=FastAPI(title="AI Trainer Feedback Analyzer")

# @app.get("/home")
# def home():
#     return "home"


# @app.post("/api/v1/analyze_trainer_feedback",response_model=TrainerResponse)
# def analyze_trainer_feedback(request:TrainerRequest):
#     result=workflow_graph.invoke({
#              "trainer_name":request.trainer_name,
#              "learner_name":request.learner_name,
#              "trainer_topic":request.trainer_topic,
#              "trainer_feedback":request.trainer_feedback,
#              "trainer_rating":request.trainer_rating
#     })
#     return TrainerResponse(
#             trainer_name=result["trainer_name"],
#             sentiments=result["sentiments"],
#             performance_level=result["performance_level"],
#             strengths=result["strengths"],
#             improvement_areas=result["improvement_areas"],
#             overall_summary=result["overall_summary"],
#             action_taken=result["action_taken"]
#         )
    