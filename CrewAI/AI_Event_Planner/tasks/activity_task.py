from crewai import Task
from agents.activity_planner_agent import activity_planner_agent
from agents.idea_generator_agent import idea_generator_agent
def create_activity_task(event_name,idea_task):

    activity_task = Task(
        description=(
            f"Create four suitable activities for "
            f"the event '{event_name}'. "
            "As per the event choose unique and enjoyable activites."
        ),

        expected_output=(
            "Four beginner-friendly and interesting event activities."
        ),

        agent=activity_planner_agent,

        context=[idea_task]
    )

    return activity_task