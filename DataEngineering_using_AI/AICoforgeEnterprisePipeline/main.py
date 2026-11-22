from fastapi import FastAPI
from routers.employee_router import(
    router as employee_router
)
from routers.knowledge_router import (
    router as knowledge_router
)

app=FastAPI(
    title="Coforge Enterprise Knowledge Project "
)

@app.get("/")
def home():
    return{
        "application":"Coforge Enterprise Pipeline",
        "status":"running"
    }

@app.get("/health")
def health():
    return{
        "status":"healthy"
    }
app.include_router(employee_router)
app.include_router(knowledge_router)