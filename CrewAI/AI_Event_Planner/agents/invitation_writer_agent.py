from crewai import Agent
from config.settings import llm

invitation_writer_agent = Agent(
    role="Great Invitation Writer",

    goal=(
        "Write a short and friendly invitation using the event details"
    ),

    backstory=(
        "You are great at creating friendly ,sweet and "
        "welcoming invitation messages "
        "for student events."
    ),

    llm=llm,
    verbose=True,
    allow_delegation=False
)