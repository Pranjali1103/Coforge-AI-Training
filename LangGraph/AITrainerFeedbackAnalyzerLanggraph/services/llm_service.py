from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


from config.settings import(
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT
)

from models.training_model import(
    TrainerRequest,TrainerResponse
)

from prompts.ai_prompt import (
    HUMAN_PROMPT,
    SYSTEM_PROMPT
)

# //create llm
llm=AzureChatOpenAI( 
    api_key=AZURE_OPENAI_API_KEY,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION
) 

structured_llm=llm.with_structured_output(TrainerResponse)

prompt=ChatPromptTemplate.from_messages(
    [
        ("system",SYSTEM_PROMPT),
        ("human",HUMAN_PROMPT)
    ]
)

chain=prompt|structured_llm

def analyze_trainer_feedback(request:TrainerRequest):
    result=chain.invoke({
      "trainer_name":request.trainer_name,
      "learner_name":request.learner_name,
      "trainer_rating":request.trainer_rating,
      "trainer_feedback":request.trainer_feedback,
      "trainer_topic":request.trainer_topic
    })
    print(type(result))
    return result