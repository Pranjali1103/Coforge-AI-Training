from crewai import Task
from config.settings import llm
from agents.quality_checker_agent import quality_checker_agent

def create_quality_check_task(
    idea_task,
    activity_task,
    invitation_task
):

    quality_check_task = Task(
        description=(
            "Check whether the theme, activities, date, "
            "and invitation are present; list any missing details. "
        ),

        expected_output=(
            "A checklist showing available details "
            "and missing details."
        ),

        agent=quality_checker_agent,

        context=[
            idea_task,
            activity_task,
            invitation_task
        ]
    )

    return quality_check_task