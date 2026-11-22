from typing import TypedDict
from langgraph.graph import StateGraph,START,END

class TrainingFeedbackState(TypedDict):
    trainer_name:str
    learner_name:str
    trainer_rating:int
    trainer_feedback:str
    trainer_topic:str
    sentiments:str
    performance_level:str
    strengths:list[str]
    improvement_areas:list[str] 
    overall_summary:str
    action_taken:str

from services.llm_service import analyze_training_feedback
from models.training_model import TrainerRequest,TrainerResponse


def analyze_training_feedback_node(state:TrainingFeedbackState):
    request=TrainerRequest(
         trainer_name=state["trainer_name"],
         learner_name=state["learner_name"],
         trainer_rating=state["trainer_rating"],
         trainer_feedback=state["trainer_feedback"],
         trainer_topic=state["trainer_topic"]
    )
    result=analyze_training_feedback(request)
    return{
        "sentiments":result.sentiments,
        "performance_level":result.performance_level,
        "strengths":result.strengths,
        "improvement_areas":result.improvement_areas,
        "overall_summary":result.overall_summary,
        "action_taken":result.action_taken
    }
def check_training_performance_level(state:TrainingFeedbackState):
    if state["performance_level"]=="Needs Improvement":
        return "Change Trainer"
    return "Continue Trainer"

def change_trainer_node(state:TrainingFeedbackState):
    return {
        "action_taken":"Change Trainer"
    }

def continue_trainer_node(state:TrainingFeedbackState):
    return {
        "action_taken":"Continue trainer"
    }

workflow=StateGraph(TrainingFeedbackState)

workflow.add_node("analyze_training_feedback_node",analyze_training_feedback_node)
workflow.add_node("change_trainer_node",change_trainer_node)
workflow.add_node("continue_trainer_node",continue_trainer_node)

workflow.add_edge(START,"analyze_training_feedback_node")
workflow.add_conditional_edges("analyze_training_feedback_node",
                               check_training_performance_level,
                               {
                                   "Change Trainer":"change_trainer_node",
                                   "Continue Trainer":"continue_trainer_node"
                               }
                               )

workflow.add_edge("change_trainer_node",END)
workflow.add_edge("continue_trainer_node",END)

workflow_graph=workflow.compile()

