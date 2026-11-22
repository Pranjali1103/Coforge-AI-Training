from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json
 
from AI_RetailCustomerQueryAssistant.config.settings import(
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT
)
from models.trainer_feedback_model import (
    TrainerFeedbackRequest,
    TrainerFeedbackResponse
)
from prompts.trainer_feedback_prompt import (
    HUMAN_PROMPT,
    SYSTEM_PROMPT
)

# create llm
llm = AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION
)

structured_llm = llm.with_structured_output(
    TrainerFeedbackResponse
)

# create prompt
prompt=ChatPromptTemplate.from_messages(
    [
        ("system",SYSTEM_PROMPT),
        ("human",HUMAN_PROMPT)
    ]
)

chain=prompt | structured_llm

def analyze_feedback(request:TrainerFeedbackRequest)->TrainerFeedbackResponse:
    result=chain.invoke({
        "trainer_name": request.trainer_name,
        "training_topic":request.training_topic,
        "learner_name":request.learner_name,
        "rating":request.rating,
        "feedback":request.feedback
    })
    
    return result 

    
# def llm_resposnse(request: TrainerFeedbackRequest) -> TrainerFeedbackResponse:
 
#     user_prompt = HUMAN_PROMPT.format(
#         training_topic=request.training_topic,
#         learner_name=request.learner_name,
#         rating=request.rating,
#         feedback=request.feedback
#     )
#     respnose = llm.chat.completions.create(
#         model=AZURE_OPENAI_DEPLOYMENT,
#         messages=[
#             {
#                 "user": "system",
#                 "content": SYSTEM_PROMPT
#             },
#             {
#                 "user": "user",
#                 "content": user_prompt
#             }
#         ],
#         response_format={"type": "json_object"}
#     )
 
#     ai_analyze = respnose.choices[0].content.message
 
#     if not ai_analyze:
#         return {
#             "Empty Response"
#         }
 
#     data = json.loads(ai_analyze)
 
#     return TrainerFeedbackResponse(
#         trainer_name=request.trainer_name,
#         sentiments=data["sentiments"],
#         performance_level=data["performance_level"],
#         strengths=data["strengths"],
#         improvement_areas=data["improvement_areas"],
#         recommendation=data["recommendation"],
#         overall_summary=data["overall_summary"]
#     )
