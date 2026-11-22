# imports
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select,func
from sqlalchemy.exc import IntegrityError
from models.trainingfeedback_model import TrainingFeedback
from schemas.trainingfeedback_schema import TrainingFeedbackCreate,TrainingFeedbackUpdate
from config.logger import logger


# 1. Submit a learner feedback record. 
def create_feedback(db:Session,data):

    feedback=TrainingFeedback(**data.model_dump())
    db.add(feedback)

    try:
        db.commit()
        db.refresh(feedback)
        logger.info(f"Feedback with Id {feedback.feedback_id} submitted successfully")
        return feedback
    
    except IntegrityError:
        db.rollback()
        logger.warning("Duplicate Feedback ID")
        raise HTTPException(status_code=409,detail="Feedback already exists")
    
    except Exception:
        db.rollback()
        logger.exception("Unexpected error while submitting feedback")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 2. List feedback records with pagination. 
def get_all_feedbacks(db:Session,skip:int,limit:int):

    try:
        query=select(TrainingFeedback).offset(skip).limit(limit)
        feedbacks=db.scalars(query).all()
        logger.info(f"Successfully retrieved {len(feedbacks)} feedback records")
        return feedbacks

    except Exception:

        logger.exception("Unexpected error while fetching feedback records")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 3. Get feedback by feedback ID. 
def get_feedback_by_id(db:Session,feedback_id:int):

    feedback=db.get(TrainingFeedback,feedback_id)

    if feedback is None:
        logger.warning(f"Feedback with Id {feedback_id} not found")
        raise HTTPException(status_code=404,detail="Feedback Not Found")
    
    logger.info(f"Feedback with Id {feedback_id} retrieved successfully")
    return feedback


# 4. Update an existing feedback entry. 
def update_feedback(db:Session,feedback_id:int,data:TrainingFeedbackUpdate):

    feedback=get_feedback_by_id(db,feedback_id)
    for key,value in data.model_dump().items():
        setattr(feedback,key,value)

    try:
        db.commit()
        db.refresh(feedback)
        logger.info(f"Feedback with Id {feedback_id} updated successfully")
        return feedback
    
    except IntegrityError:
        db.rollback()
        logger.warning(f"Database constraint violation while updating feedback {feedback_id}")
        raise

    except Exception:
        db.rollback()
        logger.exception(f"Unexpected error while updating feedback {feedback_id}")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 5. Delete a feedback entry. 
def delete_feedback(db:Session,feedback_id:int):
    feedback=get_feedback_by_id(db,feedback_id)
    try:
        db.delete(feedback)
        db.commit()
        logger.info(f"Feedback with Id {feedback_id} deleted successfully")
        return True 
    except Exception:
        db.rollback()
        logger.exception(f"Unexpected error while deleting feedback with Id {feedback_id}")
        raise HTTPException(status_code=500,detail="Internal Server Error")

# 6. Filter feedback by trainer name. 
def get_feedback_by_trainer(db:Session,trainer_name:str):
    query=select(TrainingFeedback).where(TrainingFeedback.trainer_name==trainer_name)
    feedbacks=db.scalars(query).all()

    if not feedbacks:
        logger.warning(f"No feedback found for trainer {trainer_name}")
        raise HTTPException(status_code=404,detail="No feedback found for this trainer")
    
    logger.info(f"Retrieved {len(feedbacks)} feedback records for trainer {trainer_name}")
    return feedbacks

# 7. Filter feedback by course name. 
def get_feedback_by_course(db:Session,course_name:str):

    query=select(TrainingFeedback).where(TrainingFeedback.course_name==course_name)
    feedbacks=db.scalars(query).all()

    if not feedbacks:
        logger.warning(f"No feedback found for course {course_name}")
        raise HTTPException(status_code=404,detail="No feedback found for this course")

    logger.info(f"Retrieved {len(feedbacks)} feedback records for course {course_name}")
    return feedbacks


# 8. Calculate average trainer rating for each trainer. 
def get_average_trainer_rating(db:Session):

    try:
        query=select(TrainingFeedback.trainer_name,func.avg(TrainingFeedback.trainer_rating)
                .label("average_rating")).group_by(TrainingFeedback.trainer_name)
        ratings=db.execute(query).all()
        result=[]
        for trainer,rating in ratings:
                 result.append({
                      "trainer_name":trainer,
                      "average_rating":rating
                  }) 
        logger.info(f"Average trainer rating calculated for {len(result)} trainers")
        return result
    
    except Exception:
        logger.exception("Unexpected error while calculating average trainer rating")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 9. Identify low-rated sessions where any rating is 2 or below. 
def get_low_rated_sessions(db:Session):

    try:
        query=select(TrainingFeedback).where(
            (TrainingFeedback.content_rating<=2) |
            (TrainingFeedback.trainer_rating<=2) |
            (TrainingFeedback.hands_on_rating<=2)
        )
        feedbacks=db.scalars(query).all()
        if not feedbacks:
            logger.warning("No low-rated sessions found")
            raise HTTPException(status_code=404,detail="No low-rated sessions found")
        logger.info(f"Retrieved {len(feedbacks)} low-rated sessions")
        return feedbacks

    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error while fetching low-rated sessions")
        raise HTTPException(status_code=500,detail="Internal Server Error") 


# 10. Calculate recommendation percentage for a selected course. 
def get_recommendation_percentage(db:Session,course_name:str):

    try:
        feedbacks=get_feedback_by_course(db,course_name)

        total_feedbacks=len(feedbacks)
        #recommend_count=sum(feedback.would_recommend for feedback in feedbacks)
        recommend_count=0
        for feedback in feedbacks:
            if feedback.would_recommend:
                recommend_count+=1

        recommendation_percentage=(recommend_count/total_feedbacks)*100
        logger.info(f"Recommendation percentage calculated for course {course_name}")
        return{
        "course_name":course_name,
        "recommendation_percentage":round(recommendation_percentage,2)
        }

    except HTTPException:
        raise
    
    except Exception:
        logger.exception(f"Unexpected error while calculating recommendation percentage for course {course_name}")
        raise HTTPException(status_code=500,detail="Internal Server Error")


    



    


