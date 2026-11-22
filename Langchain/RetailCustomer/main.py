from fastapi import FastAPI

from prompts.customer_prompt import SYSTEM_PROMPT,HUMAN_PROMPT
from models.customer_model import CustomerResponse,CustomerRequest,CustomerAnalysis
from services.customer_service import analyze_customer_query

app=FastAPI(title="AI Retail Customer Query Assistant")

@app.post("/api/v1/analyze-query",response_model=CustomerResponse)
def  analyze_query(request:CustomerRequest):
    return analyze_customer_query(request)

