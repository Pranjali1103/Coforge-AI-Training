from crewai import Agent
from config.settings import llm

quiz_creator_agent=Agent(
    role="Quiz Creator",
    goal=(
    "Create a beginner friendly quiz on Python topics"
    ),
    backstory=(
        "You are an experienced quiz creator." 
        "Prepare a quiz for beginners to test"
        "their understanding in Python topics"
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False

)