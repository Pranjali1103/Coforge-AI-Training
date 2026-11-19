from pydantic import BaseModel,Field,ConfigDict
from datetime import date


class TrainingFeedbackBase(BaseModel):
    learner_name:str=Field(min_length=2)
    trainer_name :str=Field(min_length=2)
    course_name :str=Field(min_length=2)
    session_date:date
    content_rating :int =Field(ge=1,le=5)
    trainer_rating:int =Field(ge=1,le=5)
    hands_on_rating :int =Field(ge=1,le=5)
    comments:str | None=None
    would_recommend:bool


class TrainingFeedbackCreate(TrainingFeedbackBase):
    pass


class TrainingFeedbackUpdate(TrainingFeedbackBase):
    pass


class TrainingFeedbackResponse(TrainingFeedbackBase):
    feedback_id:int
    model_config=ConfigDict(from_attributes=True)

    