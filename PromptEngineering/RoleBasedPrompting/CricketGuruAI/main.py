from fastapi import FastAPI
from router.cricket_router import router

app=FastAPI(
    title="Cricket Guru AI"
)
app.include_router(router)