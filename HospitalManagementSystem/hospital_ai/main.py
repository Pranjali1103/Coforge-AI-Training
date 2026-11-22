from fastapi import FastAPI
from routers.hospital_router import router

app = FastAPI(
    title="AI Hospital Management System"
)

app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }