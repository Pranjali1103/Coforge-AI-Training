from openai import OpenAI
from config.settings import(AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT)
from models.ai_model import SupportTicketRequest,SupportTicketResponse
from prompts.ai_prompt import SYSTEM_PROMPT,HUMAN_PROMPT
import json

llm = OpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    base_url=f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/v1/"
)
def generate_support_ticket_triage(request:SupportTicketRequest)->SupportTicketResponse: 
    user_prompt=HUMAN_PROMPT.format(
            ticket_id=request.ticket_id,
            employee_name=request.employee_name,
            department=request.department,
            issue_description=request.issue_description
    )
    response=llm.responses.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        instructions=SYSTEM_PROMPT,
        input=user_prompt
    )
    ai_text=response.output_text
    response_dict=json.loads(ai_text)
    print(response_dict)
    return SupportTicketResponse(**response_dict)
