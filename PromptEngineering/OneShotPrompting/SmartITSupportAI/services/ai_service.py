from openai import AzureOpenAI
from models.request_model import ITSupportRequest
from models.response_model import ITSupportResponse
from models.analysis_model import ITSupportAnalysis
from config.settings import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT
)
from prompts.one_shot_prompt import HUMAN_PROMPT,SYSTEM_PROMPT
import json
from fastapi import HTTPException

llm=AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def analyze_ticket(request:ITSupportRequest)->ITSupportResponse:
    user_prompt=HUMAN_PROMPT.format(
        ticket_id=request.ticket_id,
        employee_id=request.employee_id,
        employee_name=request.employee_name,
        department=request.department,
        issue_description=request.issue_description,
        affected_system=request.affected_system
    )
    response=llm.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },
            {
                "role":"user",
                "content":user_prompt
            }
        ],
        response_format={"type":"json_object"}
    )

    ai_text=response.choices[0].message.content

    if not ai_text:
        raise HTTPException(status_code=500,detail="LLM returned empty response")

    try:
        ai_analysis=ITSupportAnalysis(**json.loads(ai_text))
    except json.JSONDecodeError:
        raise HTTPException(status_code=500,detail="Invalid JSON returned by LLM")
    except Exception:
        raise HTTPException(status_code=500,detail="Invalid LLM response")

    if ai_analysis.priority_level in ["High","Critical"]:
        escalation_required = True
    else:
        escalation_required = False
    return ITSupportResponse(
        ticket_id=request.ticket_id,
        ticket_status="Analyzed",
        analysis=ai_analysis,
        recommended_actions=ai_analysis.troubleshooting_steps,
        escalation_required=escalation_required,
        ai_summary=f"{request.employee_name} has {ai_analysis.issue_category} issue with {ai_analysis.priority_level} priority impacting work on {ai_analysis.impact_level.lower()} level "
    )
    
           

        