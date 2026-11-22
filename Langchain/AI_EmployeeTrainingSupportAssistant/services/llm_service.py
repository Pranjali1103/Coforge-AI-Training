from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from prompts.ai_prompt import SYSTEM_PROMPT,HUMAN_PROMPT
from models.employee_model import (
    TrainingRequest,
    TrainingAnalysis,
    TrainingResponse
)

from AI_RetailCustomerQueryAssistant.config.settings import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT
)

llm = AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT
)

structured_llm = llm.with_structured_output(TrainingResponse)


prompt=ChatPromptTemplate.from_messages([
    ("system",SYSTEM_PROMPT),
    ("human",HUMAN_PROMPT)
])

chain = prompt | structured_llm


def analyze_training(request: TrainingRequest):

    result = chain.invoke({
        "employee_id": request.employee_id,
        "employee_name": request.employee_name,
        "topic": request.topic,
        "question": request.question
    })

    return result