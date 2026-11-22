from fastapi import FastAPI
from routers.training_router import router

app=FastAPI(
    title="Coforge Training Mentor AI"
)
app.include_router(router)