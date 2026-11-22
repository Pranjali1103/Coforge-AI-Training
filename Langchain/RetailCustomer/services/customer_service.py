from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from config.settings import(
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT
)
from models.customer_model import CustomerAnalysis,CustomerRequest,CustomerResponse
from prompts.customer_prompt import SYSTEM_PROMPT,HUMAN_PROMPT

llm=AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    api_version=AZURE_OPENAI_API_VERSION
)

prompt=ChatPromptTemplate.from_messages([
    ("system",SYSTEM_PROMPT),
    ("human",HUMAN_PROMPT)
])

structured_llm=llm.with_structured_output(CustomerAnalysis)
chain=prompt | structured_llm

def analyze_customer_query(request:CustomerRequest)->CustomerResponse:
    result=chain.invoke({
        "customer_id":request.customer_id,
        "customer_name":request.customer_name,
        "product_name":request.product_name,
        "query": request.query
    })
    return CustomerResponse(
        customer_id=request.customer_id,
        customer_name=request.customer_name,
        analysis=result,
        reply="We apologize for the inconvenience. Our team is reviewing your issue regarding the product.",
        next_action="Customer support team will contact the customer within 24 hours.",
        status="success"
    )

