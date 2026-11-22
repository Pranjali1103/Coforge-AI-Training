from fastapi import FastAPI

from models.cafeteria_models import (
    CafeteriaRequest,
    CafeteriaResponse
)

from services.cafeteria_service import (
    analyze_cafeteria_request
)

app = FastAPI(
    title="AI Cafeteria Menu Guidance Assistant"
)




@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post(
    "/cafeteria/recommend",
    response_model=CafeteriaResponse
)
def cafeteria_recommend(
    request: CafeteriaRequest
):
    return analyze_cafeteria_request(request)