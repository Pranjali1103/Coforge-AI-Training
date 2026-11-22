from crewai import Task
from agents.invitation_writer_agent import invitation_writer_agent


def create_invitation_task(
    event_name,
    date,
    audience,
    activity_task
):

    invitation_task = Task(
        description=(
            f"Write a short invitation for the event {event_name}"
            f"whose date is {date}."
            f"The audience is {audience}. "
            "Use event details and activities."
        ),

        expected_output=(
            "want a short and friendly invitation message."
        ),

        agent=invitation_writer_agent,

        context=[activity_task]
    )

    return invitation_task