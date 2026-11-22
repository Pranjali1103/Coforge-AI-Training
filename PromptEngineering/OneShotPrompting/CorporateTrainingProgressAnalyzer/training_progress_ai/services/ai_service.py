from openai import AzureOpenAI
from fastapi import HTTPException
from config.settings import(
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT)
from models.request_model import LearnerProgressRequest
from models.analysis_model import LearnerProgressAnalysis
from models.response_model import LearnerProgressResponse
from prompts.one_shot_prompt import SYSTEM_PROMPT,HUMAN_PROMPT
import json


llm=AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)


def analyze_progress(request:LearnerProgressRequest)->LearnerProgressResponse:

    if request.assignments_assigned == 0:
        completion_percentage=0
    else :
        completion_percentage=(request.assignments_completed/
                               request.assignments_assigned)*100
    
    user_prompt=HUMAN_PROMPT.format(
        learner_id=request.learner_id,
        learner_name=request.learner_name,
        training_program=request.training_program,
        topics_completed=request.topics_completed,
        assignments_assigned=request.assignments_assigned,
        assignments_completed=request.assignments_completed,
        attendance_percentage=request.attendance_percentage,
        coding_assessment_score=request.coding_assessment_score,
        trainer_feedback=request.trainer_feedback,
        completion_percentage=completion_percentage
    )

    response=llm.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },
            {
                "role":"user",
                "content":user_prompt
            }
        ],
        response_format={"type":"json_object"}
    ) 

    ai_text=response.choices[0].message.content

    if not ai_text:
        raise HTTPException(
            status_code=500,
            detail="LLM returned empty response"
        )

    try:
        ai_analysis=LearnerProgressAnalysis(**json.loads(ai_text))
    except json.JSONDecodeError:
        raise HTTPException(status_code=500,detail="Invalid JSON returned by LLM")
    except Exception:
        raise HTTPException(status_code=500,detail="Invalid LLM response")
    

    recommended_practice=[]

    for topic in ai_analysis.weak_topics:
        recommended_practice.append(f"Practice {topic}")

    # recommended_practice=[f"Practice {topic}" for topic in ai_analysis.weak_topics]
    
    return LearnerProgressResponse(
        learner_id =request.learner_id,
        learner_name=request.learner_name,
        analysis=ai_analysis,
        recommended_practice=recommended_practice,
        next_learning_plan=f"Improvement needed : {ai_analysis.improvement_priority}",
        trainer_recommendation=f"Focus on improving these topics:{ai_analysis.weak_topics}",
        ai_summary=(f"{request.learner_name} is at {ai_analysis.learning_level} level having strong grip on {ai_analysis.strong_topics}  with  readiness score :{ai_analysis.readiness_score}")
                         
    ) 