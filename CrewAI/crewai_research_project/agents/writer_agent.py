from crewai import Agent
from config.settings import llm

writer_agent=Agent(
    role="Professional Writer",
    goal="Write the insights and results obtained in  " \
    "a professional and easy to understand langauage",
    backstory="You are a professioanl writer and have " 
    " written so many research books for various companies" \
    "in an easy and friendly language",
    llm=llm,
    verbose=True,
    allow_delegation=False
)