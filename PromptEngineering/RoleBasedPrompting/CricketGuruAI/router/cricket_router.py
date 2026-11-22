from fastapi import APIRouter
from services.cricket_service import answer_cricket_question
from models.cricket_model import (
    CricketRequest,
    CricketResponse
)

router=APIRouter(
    prefix="/api/cricket",
    tags=["Cricket Guru AI"]
)


@router.get("/health")
def healthy():
    return{
        "status":"healthy"
    }


@router.get("/role")
def role():
    return {
        "role": "Indian Cricket AI Expert",
    }


@router.post("/ask",response_model=CricketResponse)
def cricket_question(request:CricketRequest)->CricketResponse:
    response=answer_cricket_question(request)
    return response