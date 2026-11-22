from crewai import Agent
from config.settings import llm

quality_checker_agent = Agent(
    role="Quality Checker",

    goal=(
        "Check whether all required event "
        "details are present."
    ),

    backstory=(
        "You review event plans and identify "
        "missing information."
    ),

    llm=llm,
    verbose=True,
    allow_delegation=False
)