from crewai import Task
from agents.idea_generator_agent import idea_generator_agent


def create_event_idea_task( event_name,date,audience):

    idea_task = Task(
        description=(
            f"Generate a simple event theme for the event "
            f"'{event_name}'. "
            f"The date is {date}. "
            f"The target audience is {audience}. "
            "Suggest one suitable theme."
        ),

        expected_output=(
            "One well-structured and creative event theme."
        ),

        agent=idea_generator_agent
    )

    return idea_task