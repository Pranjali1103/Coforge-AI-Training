from langchain.agents import create_agent
from langchain_openai import AzureChatOpenAI

from config.settings import(
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT
)
from prompts.ai_prompt import SALARY_SYSTEM_PROMPT

from tools.ai_tools import(
    caluclate_basic_salary,
    calculate_hra,
    calculate_da,
    calculate_gross_salary
)

def create_salary_agent():

    # Step1:Connect to Azure OpenAI
    llm=AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        api_version=AZURE_OPENAI_API_VERSION
    )

    # Step2:Register four tools
    salary_tools=[
        caluclate_basic_salary,
        calculate_hra,
        calculate_da,
        calculate_gross_salary
    ] 

    agent=create_agent(
        model=llm,
        tools=salary_tools,
        system_prompt=SALARY_SYSTEM_PROMPT
    )
    return agent