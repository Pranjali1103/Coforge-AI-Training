from typing import TypedDict
from models.maintenance_model import MaintenanceRequest,MaintenanceResponse
from services.llm_service import analyze_maintenance_question
from langgraph.graph import StateGraph,START,END

class MaintenanceState(TypedDict):
    question:str
    answer:str

def analyze_question_node(state:MaintenanceState):
    request=MaintenanceRequest(
        question=state["question"]
    )
    result=analyze_maintenance_question(request)
    return{
        "answer":result.answer
    }

workflow=StateGraph(MaintenanceState)

workflow.add_node("analyze_question_node",analyze_question_node)
workflow.add_edge(START,"analyze_question_node")
workflow.add_edge("analyze_question_node",END)

workflow_graph=workflow.compile()
