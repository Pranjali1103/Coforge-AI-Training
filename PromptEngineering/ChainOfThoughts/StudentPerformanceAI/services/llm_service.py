from openai import AzureOpenAI
from config.settings import(
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT
)
from prompts.student_prompt import (
    SYSTEM_PROMPT,
    HUMAN_PROMPT
)
from models.student_model import (
    StudentPerformanceAnalysis,
    StudentPerformanceRequest,
    StudentPerformanceResponse
)
import json

llm=AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    api_version=AZURE_OPENAI_API_VERSION
)

def analyze_student_performance(request:StudentPerformanceRequest)->StudentPerformanceResponse:
    user_prompt=HUMAN_PROMPT.format(
        student_id=request.student_id,
        student_name=request.student_name,
        python_marks=request.python_marks,
        sql_marks=request.sql_marks,
        fastapi_marks=request.fastapi_marks
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
    content=response.choices[0].message.content

    if not content:
        raise ValueError("AI returns empty response")

    student_analysis=StudentPerformanceAnalysis(**json.loads(content))

    # analysis=StudentPerformanceAnalysis(
    #    total_marks=student_analysis.total_marks,
    #    avg_marks=student_analysis.avg_marks,
    #    grade=student_analysis.grade,
    #    result=student_analysis.result,
    #    calculation_summary=student_analysis.calculation_summary,
    #    improvement_suggestion=student_analysis.improvement_suggestion
    # )

    return StudentPerformanceResponse(
        student_id=request.student_id,
        student_name=request.student_name,
        analysis=student_analysis

    )
