from pydantic import BaseModel,Field
from typing import Literal

class TrainerRequest(BaseModel):
    trainer_name:str
    trainer_name:str
    trainer_rating:int=Field(ge=1,le=5)
    trainer_feedback:str
    trainer_topic:str

class TrainerResponse(BaseModel):
    trainer_name:str
    sentiments:Literal["Positive","Neutral","Negative"]
    performance_level:Literal["Excellent","Very Good","Average","Needs Improvement"]
    strengths:list[str]
    improvement_areas:list[str] 
    overall_summary:str
    action_taken:str
                              