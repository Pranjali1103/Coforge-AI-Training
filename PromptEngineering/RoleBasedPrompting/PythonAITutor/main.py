from fastapi import FastAPI
from config.settings import AZURE_OPENAI_API_KEY,AZURE_OPENAI_DEPLOYMENT,AZURE_OPENAI_ENDPOINT
from services.llm_service import analyze_python_role_based_response
from models.model_role_based import PythonAIResponse,PythonAIRequest


app=FastAPI(title="Python AI Assistant")

@app.get("/home")
def home():
    return {"message":"Hi! Python Assistant Here"}

@app.post("/app/v1/analyzedata",response_model=PythonAIResponse)
def analyze_data(request:PythonAIRequest):
    response=analyze_python_role_based_response(request)
    return response