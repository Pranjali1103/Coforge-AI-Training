from fastapi import APIRouter
from models.request_model import ITSupportRequest
from models.response_model import ITSupportResponse
from services.ai_service import analyze_ticket

router=APIRouter(
    prefix="/api/tickets",
    tags=["IT Support Tickets"]
)

@router.get("/health")
def health():
    return {
        "status": "healthy"
    }

@router.post("/analyze",response_model=ITSupportResponse)
def analyze_support_ticket(
    request:ITSupportRequest
):
    return analyze_ticket(request)