from langgraph.graph import StateGraph, START, END
from typing import TypedDict

from models.ai_model import AstronautRequest
from services.llm_service import analyze_astronaut_mission


class AstronautState(TypedDict):
    astronaut_id: int
    astronaut_name: str
    age: int
    training_hours: int
    medical_clearance: bool
    previous_missions: int

    mission_status: str
    assigned_mission: str
    reason: str


def analyze_astronaut_mission_node(state: AstronautState):

    request = AstronautRequest(
        astronaut_id=state["astronaut_id"],
        astronaut_name=state["astronaut_name"],
        age=state["age"],
        training_hours=state["training_hours"],
        medical_clearance=state["medical_clearance"],
        previous_missions=state["previous_missions"]
    )

    result = analyze_astronaut_mission(request)

    return {
        "astronaut_id": request.astronaut_id,
        "astronaut_name": request.astronaut_name,
        "mission_status": result.mission_status,
        "assigned_mission": result.assigned_mission,
        "reason": result.reason
    }


def check_medical_clearance(state: AstronautState):

    if state["medical_clearance"] == False:
        return "Reject"

    return "Training Check"


def training_check_node(state: AstronautState):
    return state


def check_training_hours(state: AstronautState):

    if state["training_hours"] < 100:
        return "Training Required"

    return "Mission Assignment"


def training_required_node(state: AstronautState):

    return {
        "mission_status": "TRAINING_REQUIRED",
        "assigned_mission": "None",
        "reason": "Minimum 100 training hours required"
    }


def rejected_node(state: AstronautState):

    return {
        "mission_status": "REJECTED",
        "assigned_mission": "None",
        "reason": "Medical clearance failed"
    }


def assign_mission(state: AstronautState):

    if state["previous_missions"] >= 1:

        return {
            "mission_status": "APPROVED",
            "assigned_mission": "Orbital Research",
            "reason": "Experienced astronaut"
        }

    return {
        "mission_status": "APPROVED",
        "assigned_mission": "Training Mission",
        "reason": "First-time astronaut"
    }


workflow = StateGraph(AstronautState)

workflow.add_node(
    "analyze_astronaut_mission_node",
    analyze_astronaut_mission_node
)

workflow.add_node(
    "rejected_node",
    rejected_node
)

workflow.add_node(
    "training_check_node",
    training_check_node
)

workflow.add_node(
    "training_required_node",
    training_required_node
)

workflow.add_node(
    "assign_mission",
    assign_mission
)

workflow.add_edge(
    START,
    "analyze_astronaut_mission_node"
)

workflow.add_conditional_edges(
    "analyze_astronaut_mission_node",
    check_medical_clearance,
    {
        "Reject": "rejected_node",
        "Training Check": "training_check_node"
    }
)

workflow.add_conditional_edges(
    "training_check_node",
    check_training_hours,
    {
        "Training Required": "training_required_node",
        "Mission Assignment": "assign_mission"
    }
)

workflow.add_edge(
    "rejected_node",
    END
)

workflow.add_edge(
    "training_required_node",
    END
)

workflow.add_edge(
    "assign_mission",
    END
)

workflow_graph = workflow.compile()