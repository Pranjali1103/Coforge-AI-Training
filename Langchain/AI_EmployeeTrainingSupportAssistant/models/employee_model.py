from pydantic import BaseModel, Field
from typing import Literal


# Model 1
class TrainingRequest(BaseModel):
    employee_id: int = Field(gt=0)
    employee_name: str = Field(min_length=2)
    topic: str = Field(min_length=1)
    question: str = Field(min_length=10)


# Model 2
class TrainingAnalysis(BaseModel):
    category: Literal["Concept", "Coding", "Career", "Other"]
    difficulty: Literal["Beginner", "Intermediate", "Advanced"]
    priority: Literal["Low", "Medium", "High"]
    summary: str


# Model 3
class TrainingResponse(BaseModel):
    employee_id: int
    employee_name: str
    topic: str
    analysis: TrainingAnalysis
    answer: str
    recommended_action: str
    status: str