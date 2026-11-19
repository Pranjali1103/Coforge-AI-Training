from pydantic import BaseModel
from typing import Literal

class SupportTicketRequest(BaseModel):
    ticket_id:str
    employee_name:str
    department:str
    issue_description:str


class SupportTicketResponse(BaseModel):
    ticket_id:str
    category:str
    priority:Literal["Low","Medium","High","Critical"]
    issue_summary:str
    business_impact:str
    suggested_resolution_steps:list[str]
    recommended_team:str
    escalation_required:bool
    justification:str