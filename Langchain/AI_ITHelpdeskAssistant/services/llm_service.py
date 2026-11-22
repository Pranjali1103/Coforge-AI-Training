from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from prompts.ai_prompt import SYSTEM_PROMPT,HUMAN_PROMPT
from AI_RetailCustomerQueryAssistant.config.settings import(
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT
)
from models.ai_model import HelpdeskAnalysis,HelpdeskRequest,HelpdeskResponse

llm=AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

structured_llm=llm.with_structured_output(HelpdeskAnalysis)

prompt=ChatPromptTemplate.from_messages([
    ("system",SYSTEM_PROMPT),
    ("human",HUMAN_PROMPT)
])
chain=prompt|structured_llm

def analyze_helpdesk_request(request:HelpdeskRequest)-> HelpdeskResponse:
    result=chain.invoke({
        "employee_id":request.employee_id,
        "employee_name":request.employee_name,
        "issue_type":request.issue_type,
        "issue_description":request.issue_description
    })
    return HelpdeskResponse(
            employee_id = request.employee_id,
            employee_name = request.employee_name,
            analysis = result,
            # suggested_steps=[""],
            # escalation_message=" ",
            status="success"
    )
