from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from prompts.cafeteria_prompt import SYSTEM_PROMPT, HUMAN_PROMPT

from models.cafeteria_models import (
    CafeteriaAnalysis,
    CafeteriaRequest,
    CafeteriaResponse
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
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    api_version=AZURE_OPENAI_API_VERSION
)

structured_llm = llm.with_structured_output(CafeteriaAnalysis)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", HUMAN_PROMPT)
])

chain = prompt | structured_llm


def analyze_cafeteria_request(
    request: CafeteriaRequest
) -> CafeteriaResponse:

    result = chain.invoke({
        "employee_id": request.employee_id,
        "employee_name": request.employee_name,
        "food_preference": request.food_preference,
        "budget": request.budget,
        "question": request.question
    })

    analysis = CafeteriaAnalysis(
        meal_type=result.meal_type,
        budget_category=result.budget_category,
        preference_match=result.preference_match,
        summary=result.summary,
        estimated_price=result.estimated_price
    )

    return CafeteriaResponse(
        employee_id=request.employee_id,
        employee_name=request.employee_name,
        analysis=analysis,
        suggested_meal="Vegetarian Thali",
        estimated_price=result.estimated_price,
        reason=result.summary,
        status="success"
    )