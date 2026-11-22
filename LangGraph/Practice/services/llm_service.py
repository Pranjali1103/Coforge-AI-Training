from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from config.settings import(
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT
)

from models.training_model import(
    TrainerRequest,
    TrainerResponse
)
from prompts.ai_prompt import(
    SYSTEM_PROMPT,
    HUMAN_PROMPT
)

# configure llm
llm=AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT
)

structured_llm=llm.with_structured_output(TrainerResponse)

prompt=ChatPromptTemplate.from_messages([
    ("system",SYSTEM_PROMPT),
    ("human",HUMAN_PROMPT)
])

chain=prompt|structured_llm

def analyze_training_feedback(request:TrainerRequest):
    result=chain.invoke({
        "trainer_name":request.trainer_name,
        "learner_name":request.learner_name,
        "trainer_rating":request.trainer_rating,
        "trainer_feedback":request.trainer_feedback,
        "trainer_topic":request.trainer_topic
    })
    return result

    





