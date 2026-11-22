from pydantic import BaseModel

class MaintenanceRequest(BaseModel):
    question:str

class MaintenanceResponse(BaseModel):
    question:str
    answer:str