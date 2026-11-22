from langgraph.graph import StateGraph,START,END

from services.customer_service import analyze_customer_feedback
from typing import TypedDict
from models.customer_model import(CustomerResponse,CustomerRequest)

class CustomerState(TypedDict):
    customer_id:str 
    customer_name:str
    order_id:str
    rating:int
    feedback:str
    customer_id:str
    sentiment:str
    issue_category:str 
    priority:str 
    reply:str
    status:str


def analyze_customer_feedback_node(state:CustomerState):
    request=CustomerRequest(
        customer_id=state["customer_id"],
        customer_name=state["customer_name"],
        order_id=state["order_id"],
        rating=state["rating"],
        feedback=state["feedback"]
    )
    result=analyze_customer_feedback(request)
    return{
        "sentiment":result.sentiment,
        "issue_category":result.issue_category,
        "priority":result.priority,
        "reply":result.reply,
        "status":result.status
    
    }

def validate_feedback(state:CustomerState):
    if not state["customer_id"]:
        return "Ente the customer id"
    elif not state["customer_name"]:
        return "Enter the customer name"
    elif not state["order_id"]:
        return "Enter the order id"
    elif state["rating"]>5:
        return "Rating cannot be more than 5"
    elif not state["feedback"]:
        return "Feedback must be present"
    return "Validated"

def classify_feedback(state:CustomerState):
    if state["sentiment"]=="Negative":
        return "High"
    else:
        return "Normal"

def set_priority1(state:CustomerState):
     state["priority"]="High"

def set_priority2(state:CustomerState):
    state["priority"]="Normal"

def generate_reply(state:CustomerState):
    result=analyze_customer_feedback()
    state["reply"]=result.reply

workflow=StateGraph(CustomerState)

workflow.add_node("analyze_customer_feedback_node",analyze_customer_feedback_node)
workflow.add_node("validate_feedback",validate_feedback)
workflow.add_node("generate_reply",generate_reply)
workflow.add_node("set_priority1",set_priority1)
workflow.add_node("set_priority2",set_priority2)
# workflow.add_node("generate_reply",generate_reply)
workflow.add_edge(START,"analyze_customer_feedback_node")
workflow.add_conditional_edges("analyze_customer_feedback_node",
                               validate_feedback,
                               {
                                   "High":"set_priority2",
                                   "Normal":"set_priority1"
                               }
                               
                        )


workflow.add_edge("set_priority2",END)
workflow.add_edge("set_priority1",END)
workflow.add_edge("generate_reply",END)




workflow_graph=workflow.compile()






