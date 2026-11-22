from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from config.settings import(
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT
)

from models.customer_model import (
    CustomerRequest,
    CustomerResponse
)

from prompts.ai_prompt import(
    HUMAN_PROMPT,
    SYSTEM_PROMPT
)

llm=AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

structure_llm=llm.with_structured_output(CustomerResponse)

prompt=ChatPromptTemplate.from_messages([
    ("system",SYSTEM_PROMPT),
    ("human",HUMAN_PROMPT)
])

chain=prompt|structure_llm

def analyze_customer_feedback(request:CustomerRequest):
    result=chain.invoke({
        "customer_id":request.customer_id,
        "customer_name":request.customer_name,
        "order_id":request.order_id,
        "rating":request.rating,
        "feedback":request.feedback
    })
    return result