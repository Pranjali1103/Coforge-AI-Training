from pydantic import BaseModel
from typing import Any

class HospitalResponse(BaseModel):
    status: str
    response: str
    tools_used: list[str]
    data: dict[str, Any]