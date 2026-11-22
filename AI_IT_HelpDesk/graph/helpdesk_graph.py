from langgraph.graph import StateGraph,START,END
from graph.helpdesk_state import HelpdeskState
from agents.analysis_agent import  analyze_issue
from agents.resolution_agent import resolve_issue
from agents.review_agent import review_resolution

from tools.it_support_tools import create_support_ticket


def escalate_issue(state):
    ticket_result=create_support_ticket.invoke({
        "employee_id":state["employeeID"],
        "issue":state["issue"],
        "priority":state["priority"]
    })
    # Extract ticket Id from the simulated tool response
    ticket_id=ticket_result.split("Ticket iD:")[1].split(".")[0]
    return {
        "ticketId":ticket_id,
        "status":"Escalated"

    }

def generate_response(state):
    status=state["status"]
    if status!="Escalated":
        status="Resolution Suggested"
    response={
        "employeeId":state["employeeId"],
        "category":state["category"],
        "priority":state["priority"],
        "agentUsed":"Resolution Agent",
        "toolsCalled":state["toolsCalled"],
        "resolution":state["resolution"],
        "reviewStatus":state["reviewStatus"],
        "ticketId":state["ticketId"],
        "status":status
    }
    return{
        "status":status,
        "finalResponse":response
    }

#Conditional routing after analysis
def route_after_analysis(state):
    if state["priority"]=="Critical":
        return "escalate"
    return "resolve"

def route_after_review(state):
    if state["reviewStatus"]=="Approved":
        return "generate"
    return "escalate"

#Create StateGraph
workflow=StateGraph(HelpdeskState)

#Register nodes
workflow.add_node("analyze",analyze_issue)
workflow.add_node("resolve",resolve_issue)
workflow.add_node("review",review_resolution)
workflow.add_node("escalate",escalate_issue)
workflow.add_node("generate",generate_response)

#starting the edge
workflow.add_edge(START,"analyze")

#Routing after issue analysis
workflow.add_conditional_edges(
    "analyze",
    route_after_analysis,
    {
        "resolve":"resolve",
        "escalate":"escalate"
    }
)

#Resolution goes to quality review
workflow.add_edge("resolve","review")

#Routing after quality review
workflow.add_conditional_edges(
    "review",
    route_after_review,
    {
        "generate":"generate",
        "escalate":"escalate"
    }
)



#Escalation goes to final reponse
workflow.add_edge("escalate","generate")

#END workflow
workflow.add_edge("generate",END)

# Compile the graph
helpdesk_graph=workflow.compile()


