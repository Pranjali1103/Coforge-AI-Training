from fastapi import FastAPI
from models.order_model import OrderRequest
from graphs.cafeteria_graph import cafeteria_graph

app = FastAPI()


@app.post("/order")
def place_order(request: OrderRequest):

    initial_state = {
        "employee_id": request.employee_id,
        "employee_name": request.employee_name,
        "items": [item.model_dump() for item in request.items],

        "order_id": "ORD01",
        "invoice_id": "INV01",

        "subtotal": 0,
        "gst": 0,
        "total": 0,

        "elapsed_minutes": 25,

        "priority": "",
        "escalation_message": "",

        "status": ""
    }

    result = cafeteria_graph.invoke(initial_state)

    return result