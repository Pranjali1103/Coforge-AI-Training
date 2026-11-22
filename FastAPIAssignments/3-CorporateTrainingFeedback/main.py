from fastapi import FastAPI
from config.database import Base,engine,SessionLocal
from schemas.trainingfeedback_schema import TrainingFeedbackCreate,TrainingFeedbackUpdate,TrainingFeedbackResponse
from services import trainingfeedback_service as service


app=FastAPI(title="Corporate Training Feedback API ")

Base.metadata.create_all(bind=engine)


@app.post("/createFeedback",response_model=TrainingFeedbackResponse,status_code=201)
def create_feedback(feedback:TrainingFeedbackCreate):

    db=SessionLocal()
    try:
        return service.create_feedback(db,feedback)
    finally:
        db.close()


@app.get("/getAllFeedbacks",response_model=list[TrainingFeedbackResponse])
def get_all_feedbacks(skip:int=0,limit:int=10):

    db=SessionLocal()
    try:
        return service.get_all_feedbacks(db,skip,limit)
    finally:
        db.close()



@app.get("/getFeedbackById/{feedback_id}",response_model=TrainingFeedbackResponse)
def get_feedback_by_id(feedback_id:int):
    db=SessionLocal()
    try:
        return service.get_feedback_by_id(db,feedback_id)
    finally:
        db.close()


@app.put("/updateFeedback/{feedback_id}",response_model=TrainingFeedbackResponse)
def update_feedback(feedback_id:int,feedback:TrainingFeedbackUpdate):
    db=SessionLocal()
    try:
        return service.update_feedback(db,feedback_id,feedback)
    finally:
        db.close()


@app.delete("/deleteFeedback/{feedback_id}")
def delete_feedback(feedback_id:int):
    db=SessionLocal()
    try:
        return service.delete_feedback(db,feedback_id)

    finally:
        db.close()

@app.get("/getFeedbackByTrainer/{trainer_name}",response_model=list[TrainingFeedbackResponse])
def get_feedback_by_trainer(trainer_name:str):
    db=SessionLocal()
    try:
        return service.get_feedback_by_trainer(db,trainer_name)
    finally:
        db.close()


@app.get("/getFeedbackByCourse/{course_name}",response_model=list[TrainingFeedbackResponse])
def get_feedback_by_course(course_name: str):
    db = SessionLocal()
    try:
        return service.get_feedback_by_course(db,course_name)
    finally:
        db.close()


@app.get("/averageTrainerRating")
def calculate_avg_trainer_rating():
    db=SessionLocal()
    try:
        return service.get_average_trainer_rating(db)
    finally:
        db.close()

    

@app.get("/lowRatedSessions",response_model=list[TrainingFeedbackResponse])
def  get_low_rated_sessions():
    db=SessionLocal()
    try:
        return service.get_low_rated_sessions(db)
    finally:
        db.close()



@app.get("/recommendationPercentage/{course_name}")
def get_recommendation_percentage(course_name:str):
    db=SessionLocal()
    try:
        return service.get_recommendation_percentage(db,course_name)
    finally:
        db.close()


