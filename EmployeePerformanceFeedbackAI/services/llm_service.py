from openai import OpenAI
import json
from prompts.ai_prompt import SYSTEM_PROMPT,HUMAN_PROMPT
from models.ai_model import EmployeeFeedbackRequest,EmployeeFeedbackResponse
from config.settings import (AZURE_OPENAI_API_KEY,AZURE_OPENAI_DEPLOYMENT,AZURE_OPENAI_ENDPOINT)

llm=OpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    base_url=f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/v1"

)

def generate_employee_performance_feedback(request:EmployeeFeedbackRequest)->EmployeeFeedbackResponse:

    user_prompt=HUMAN_PROMPT.format(
        employee_name=request.employee_name,
        reviewer_name=request.reviewer_name,
        project_name=request.project_name,
        performance_rating=request.performance_rating,
        feedback=request.feedback
    )
    response=llm.responses.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        instructions=SYSTEM_PROMPT,
        input=user_prompt
    )
    ai_text=response.output_text
    data=json.loads(ai_text)
    return EmployeeFeedbackResponse(**data)