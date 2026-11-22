from fastapi import APIRouter

from models.request_model import HospitalRequest
from models.response_model import HospitalResponse

from services.agent_service import process_request

router = APIRouter(
    prefix="/hospital",
    tags=["Hospital"]
)


@router.post(
    "/ask",
    response_model=HospitalResponse
)
def ask_hospital(request: HospitalRequest):

    result = process_request(request.message)

    return result