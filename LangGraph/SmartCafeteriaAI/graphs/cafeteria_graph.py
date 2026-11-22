from typing import TypedDict
from config.menu import MENU
from langgraph.graph import START,END,StateGraph

class CafeteriaState(TypedDict):

    employee_id:str
    employee_name:str

    items:list

    order_id:str
    invoice_id:str

    subtotal:float
    gst:float
    total:float

    elapsed_minutes:int

    priority:str
    escalation_message:str

    status:str


def validate_order(state:CafeteriaState):
    if not state["employee_id"]:
        raise ValueError("Employee ID is required")

    if not state["employee_name"]:
        raise ValueError("Employee Name is required")
    for item in state["items"]:
        if item["food_name"] not in MENU:
            raise ValueError (f"{item['food_name']} not available")
    
        if item["quantity"]<=0:
            raise ValueError(f"Invalid quantity") 
    return state



def generate_invoice(state:CafeteriaState):

    subtotal=0
    gst_pc=0.05

    for item in state["items"]:
        price=MENU[item["food_name"]]
        subtotal+=(price*item["quantity"])

    gst_amt=subtotal*gst_pc
    total_amt=subtotal+gst_amt
    state["subtotal"]=subtotal
    state["gst"]=gst_amt
    state["total"]=total_amt
    return state

def check_delivery(state:CafeteriaState):
    elapsed=state["elapsed_minutes"]

    if elapsed<=20:
        state["priority"] = "NORMAL"

    elif elapsed <= 30:
        state["priority"]="HIGH"

    else:
        state["priority"]="CRITICAL"   
    return state

def  should_escalate (state:CafeteriaState):
    if state["priority"]=="NORMAL":
        return "confirm"
    return "escalate"

def escalate_order(state:CafeteriaState):
    if state["priority"]=="HIGH":
        state["escalation_message"]="Notify Cafeteria Supervisor  "
    elif state["priority"] == "CRITICAL":
        state["escalation_message"]="Notify Cafeteria Manager"

    return state


def confirm_order(state:CafeteriaState):

    state["status"] = "Order Confirmed"

    return state


workflow=StateGraph(CafeteriaState)

workflow.add_node("validate_order",validate_order)
workflow.add_node("generate_invoice",generate_invoice)
workflow.add_node("check_delivery",check_delivery)
workflow.add_node("confirm_order",confirm_order)
workflow.add_node("escalate_order",escalate_order)


workflow.add_edge(START,"validate_order")
workflow.add_edge("validate_order","generate_invoice")

workflow.add_edge("generate_invoice","check_delivery")

workflow.add_conditional_edges(
    "check_delivery",
    should_escalate,
    {
        "confirm":"confirm_order",
        "escalate":"escalate_order"
    }
)

workflow.add_edge("confirm_order",END)
workflow.add_edge("escalate_order",END)


cafeteria_graph=workflow.compile()
