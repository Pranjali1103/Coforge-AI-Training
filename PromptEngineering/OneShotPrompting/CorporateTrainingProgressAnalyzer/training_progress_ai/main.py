from fastapi import FastAPI
from routers.analysis_router import router

app=FastAPI(
    title="Corporate Training Progress Analyzer "
)
app.include_router(router)