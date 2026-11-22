<<<<<<< HEAD
from fastapi import FastAPI
from models.ai_model import SupportTicketResponse,SupportTicketRequest
from services.llm_service import generate_support_ticket_triage

app=FastAPI(title=" Customer Support Ticket Triage AI ")

@app.get("/Home")
def home():
    return {
        "message": "Customer Support Ticket Triage AI is working"
    }

@app.post("/api/v1/triage-ticket",response_model=SupportTicketResponse)
def triage_ticket(request:SupportTicketRequest):
    response=generate_support_ticket_triage(request)
=======
from fastapi import FastAPI
from models.ai_model import SupportTicketResponse,SupportTicketRequest
from services.llm_service import generate_support_ticket_triage

app=FastAPI(title=" Customer Support Ticket Triage AI ")

@app.get("/Home")
def home():
    return {
        "message": "Customer Support Ticket Triage AI is working"
    }

@app.post("/api/v1/triage-ticket",response_model=SupportTicketResponse)
def triage_ticket(request:SupportTicketRequest):
    response=generate_support_ticket_triage(request)
>>>>>>> 4815cfea9516beac7269297805b69865a2a3d05b
    return response