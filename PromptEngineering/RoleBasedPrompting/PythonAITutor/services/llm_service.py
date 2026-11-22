from openai import OpenAI
from models.model_role_based import PythonAIRequest,PythonAIResponse

from prompts.prompt_role_based import SYSTEM_PROMPT,HUMAN_PROMPT

from config.settings import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT)

import json

llm=OpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    base_url=f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/v1/"
)

def analyze_python_role_based_response(request:PythonAIRequest)->PythonAIResponse:
    user_prompt=HUMAN_PROMPT.format(
        learner_name=request.learner_name,
        question=request.question,
        experience_level=request.experience_level
    )
    response=llm.responses.parse(
        model=AZURE_OPENAI_DEPLOYMENT,
        instructions=SYSTEM_PROMPT,
        input=user_prompt,
        text_format=PythonAIResponse
    )

    ai_text=response.output_text
    data=json.loads(ai_text)

    return PythonAIResponse(**data)