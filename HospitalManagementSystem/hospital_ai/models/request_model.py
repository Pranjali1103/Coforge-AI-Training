from pydantic import BaseModel, Field

class HospitalRequest(BaseModel):
    message: str = Field(min_length=1)
    user_role: str = Field(min_length=1)