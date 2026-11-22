from openai import OpenAI
from config.settings import AZURE_OPENAI_API_KEY,AZURE_OPENAI_API_VERSION,AZURE_OPENAI_DEPLOYMENT,AZURE_OPENAI_ENDPOINT
from models.training_model import(
    TrainingRequest,
    TrainingResponse
)
from fastapi import HTTPException

from prompts.training_prompt import(
    SYSTEM_PROMPT,
    HUMAN_PROMPT
)

llm=OpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    base_url=f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/v1/"
)

def analyze_training_question(request: TrainingRequest) -> TrainingResponse:
    user_prompt=HUMAN_PROMPT.format(
        employee_name=request.employee_name,
        experience_level=request.experience_level,
        question=request.question
    )
    try:
        response=llm.responses.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            instructions=SYSTEM_PROMPT,
            input=user_prompt
        )
        ai_text=response.output_text
        if not ai_text:
            raise HTTPException(status_code=500,detail="LLM returned empty response")
        return TrainingResponse(
            employee_name=request.employee_name,
            role="Coporate IT Training Assistant",
            answer=ai_text
        )
    except Exception:
        raise HTTPException(status_code=500,detail="Failed to generate training response")