from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json

from config.settings import(
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT
)
from models.incident_model import(
    IncidentRequest,
    IncidentAnalysis,
    IncidentResponse
)
from prompts.incident_prompt import(
    SYSTEM_PROMPT,
    HUMAN_PROMPT
)
llm=AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION
)
structured_llm=llm.with_structured_output(IncidentAnalysis)

prompt=ChatPromptTemplate.from_messages(
    [
        ("system",SYSTEM_PROMPT),
        ("human",HUMAN_PROMPT)
    ]
)
chain=prompt|structured_llm

def analyze_it_incident(request:IncidentRequest):
    result=chain.invoke({
        "employee_id":request.employee_id,
        "employee_name": request.employee_name,
        "department": request.department,
        "issue": request.issue
    })
    return result 