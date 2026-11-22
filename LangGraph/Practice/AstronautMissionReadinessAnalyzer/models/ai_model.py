from pydantic import BaseModel,Field
from typing import Literal

class  AstronautRequest(BaseModel):
       
        astronaut_id:int=Field(gt=0)
        astronaut_name :str=Field(min_length=1)
        age:int=Field(ge=18 ,le=65)
        training_hours :int =Field(ge=0)
        medical_clearance :bool 
        previous_missions :int=Field(ge=0)

class AstronautResponse(BaseModel):
        astronaut_id:int
        astronaut_name:str
        mission_status:Literal["APPROVED" ,"TRAINING_REQUIRED" ,"REJECTED" ]
        assigned_mission :Literal["Orbital Research","Training Mission","None"]
        reason:str

