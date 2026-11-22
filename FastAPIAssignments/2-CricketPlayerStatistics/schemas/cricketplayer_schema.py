from pydantic import BaseModel,Field,ConfigDict
from typing import Literal


class CricketPlayerBase(BaseModel):
    player_name:str=Field(min_length=2)
    team_name:str=Field(min_length=2)
    role:Literal["Batter","Bowler","All-Rounder", "Wicketkeeper"]
    matches_played:int=Field(ge=0)
    total_runs:int=Field(ge=0)
    wickets_taken: int = Field(ge=0)
    balls_faced:int=Field(ge=0)
    catches:int=Field(ge=0)

class CricketPlayerCreate(CricketPlayerBase):
    pass

class CricketPlayerUpdate(BaseModel):
    matches_played:int=Field(ge=0)
    total_runs:int=Field(ge=0)
    wickets_taken: int = Field(ge=0)
    balls_faced:int=Field(ge=0)
    catches:int=Field(ge=0)

class CricketPlayerResponse(CricketPlayerBase):
    player_id:int
    model_config=ConfigDict(from_attributes=True)