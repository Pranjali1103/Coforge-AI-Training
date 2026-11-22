from crewai import Agent
from config.settings import llm

study_planner_agent=Agent(
    role="Study Planner Specialist",

    goal=(
        "Create a simple, short  and "
        "effective study plan for beginners" 
        "to help them learn a Python topic easily"
    ),

    backstory=(
        "You are an expert in creating a study plan" 
        "for beginners.You have created study plan"
        "for so many stuidents to strengthen their concepts " 
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False

)