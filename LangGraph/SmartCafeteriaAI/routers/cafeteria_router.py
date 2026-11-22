from fastapi import APIRouter
from config.menu import MENU


router=APIRouter(
    prefix="/cafeteria",
    tags=["Cafeteria"]
)

@router.get("/menu")
def get_menu():
    return MENU

@router.get("/health")
def health():
    return {
        "status": "healthy"
    }