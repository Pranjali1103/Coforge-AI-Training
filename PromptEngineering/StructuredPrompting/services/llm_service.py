from openai import AzureOpenAI
from prompts.ai_prompt import SYSTEM_PROMPT,HUMAN_PROMPT
from models.ai_model import(
    LearnerAnalysis,
    LearnerRequest,
    LearnerResponse
)
from config.settings import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT
)
import json

llm=AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def analyze_learner_performance(request:LearnerRequest)->LearnerResponse:

    if request.assignmentsCompleted > request.totalAssignments:
        raise ValueError("Assignments completed cannot be greater than the assigned assignments")

    completion_pc=(request.assignmentsCompleted/request.totalAssignments)*100
    
    average_score=(request.pythonScore+request.fastapiScore+request.sqlScore)/3
    
    if average_score>=85:
        performance_level="EXCELLENT"
    elif average_score>=75:
        performance_level="GOOD"
    elif average_score>=50:
        performance_level="AVERAGE"
    else:
        performance_level="Needs Improvement"

    scores={
        "Python":request.pythonScore,
        "SQL":request.sqlScore,
        "FastAPI":request.fastapiScore
    }

    strongest=max(scores,key=scores.get)
    weakest=min(scores,key=scores.get)
    
    user_prompt=HUMAN_PROMPT.format(
        learnerName=request.learnerName,
        department=request.department,
        pythonScore=request.pythonScore,
        sqlScore=request.sqlScore,
        fastapiScore=request.fastapiScore,
        attendancePercentage=request.attendancePercentage,
        assignmentsCompleted=request.assignmentsCompleted, 
        totalAssignments=request.totalAssignments,
        averageScore=average_score,
        performanceLevel=performance_level,
        strongestTechnology=strongest,
        weakestTechnology=weakest,
        completionPercentage=completion_pc
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
    print(ai_text)
    ai_data=json.loads(ai_text)
    print(ai_data)

    if not ai_text:
        raise ValueError("LLm returned empty response")

    ai_analysis=LearnerAnalysis(
        averageScore=average_score,
        performanceLevel=performance_level,
        strongestTechnology=strongest,
        weakestTechnology=weakest,
        technicalAssessment=ai_data["technicalAssessment"],
        recommendedLearning=ai_data["recommendedLearning"]
    )

    return LearnerResponse(
        learnerName=request.learnerName,
        department=request.department,
        analysis=ai_analysis,
        finalRecommendation=ai_data["finalRecommendation"]
    )
    