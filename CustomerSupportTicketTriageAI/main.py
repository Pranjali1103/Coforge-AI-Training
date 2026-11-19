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
    return response