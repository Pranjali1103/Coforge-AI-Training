from crewai import Agent
from config.settings import llm
from tools.leave_tool import check_leave_balance

leave_verfier=Agent(
    role="Leave Verification Specialist",
    goal=(
        "Verfiy employee information and " 
        "avaiable leave balance"
    ),
    backstory=(
        "Yoy are an employee leave verification"
        "specialist working in the HR department"
        "You verfiy employee information using"
        "the employee leave balance tool"
    ),
    tools=[check_leave_balance],
    llm=llm,
    verbose=True,
    allow_delegation=False
)