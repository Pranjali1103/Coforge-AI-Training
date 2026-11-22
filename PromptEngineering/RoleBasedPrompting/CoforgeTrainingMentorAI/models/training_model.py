from pydantic import BaseModel, Field
from typing import Literal


class TrainingRequest(BaseModel):
    employee_name: str = Field(min_length=2)
    experience_level: Literal[
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
    question: str = Field(min_length=5)


class TrainingResponse(BaseModel):
    employee_name: str
    role: str
    answer: str