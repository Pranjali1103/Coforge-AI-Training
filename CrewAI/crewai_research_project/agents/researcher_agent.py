from crewai import Agent
from config.settings import llm

research_agent=Agent(
    role="Top Researcher ",
    goal="Do the in depth research of the topic given " 
    "to get meaningful insights",
    backstory="You are a top researcher of Technical world" 
    "You have done researches for various technical companies" 
    "and have generated accurate insights",
    llm=llm,
    verbose=True,
    allow_delegation=False
)