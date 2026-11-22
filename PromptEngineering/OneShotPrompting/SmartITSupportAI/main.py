from fastapi import FastAPI
from routers.ticket_router import router

app=FastAPI(
    title="Smart IT Support AI"
)

app.include_router(router)