from openai import OpenAI
from models.cricket_model import(
    CricketRequest,CricketResponse
)
from config.settings import(
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT
)
from fastapi import HTTPException
from prompts.cricket_prompt import SYSTEM_PROMPT,HUMAN_PROMPT


llm=OpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    base_url=f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/v1/"
)

def answer_cricket_question(request:CricketRequest)->CricketResponse:
    user_prompt=HUMAN_PROMPT.format(
        user_name=request.user_name,
        knowledge_level=request.knowledge_level,
        question=request.question
    )

    response=llm.responses.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        instructions=SYSTEM_PROMPT,
        input=user_prompt
    )
    ai_text=response.output_text

    if not ai_text:
        raise HTTPException(status_code=500,detail="LLM returned empty response")

    return CricketResponse(
        user_name=request.user_name,
        role="Indian Cricket AI Expert",
        answer=ai_text
    )
