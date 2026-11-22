from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from config.settings import (
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION
)
from models.ai_model import AstronautRequest,AstronautResponse

from prompts.ai_prompt import SYSTEM_PROMPT,HUMAN_PROMPT

llm=AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

structured_llm=llm.with_structured_output(AstronautResponse)

prompt=ChatPromptTemplate.from_messages([
    ("system",SYSTEM_PROMPT),
    ("human",HUMAN_PROMPT)
])

chain=prompt|structured_llm

def analyze_astronaut_mission(request:AstronautRequest):
    result=chain.invoke({
         "astronaut_id":request.astronaut_id,
         "astronaut_name":request.astronaut_name,
         "age":request.age,
         "training_hours":request.training_hours,
         "medical_clearance":request.medical_clearance,
         "previous_missions":request.previous_missions
    })
    return result