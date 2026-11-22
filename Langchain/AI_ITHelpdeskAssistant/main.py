from fastapi import FastAPI

from models.ai_model import (
    HelpdeskResponse,HelpdeskAnalysis,HelpdeskRequest
)

from services.llm_service import (
    analyze_helpdesk_request
)

app = FastAPI(
    title="AI IT HELP DESK Assistant"
)

@app.get("/")
def get_home():
   return "home"


@app.post("/api/v1/analyze_helpdesk",response_model=HelpdeskResponse)
def analyze_helpdesk(request:HelpdeskRequest):
    return analyze_helpdesk_request(request)