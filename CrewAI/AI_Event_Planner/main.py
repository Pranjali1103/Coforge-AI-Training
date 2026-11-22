from crewai import Crew, Process

from tasks.idea_task import create_event_idea_task
from tasks.activity_task import create_activity_task
from tasks.invitation_task import create_invitation_task
from tasks.quality_task import create_quality_check_task

from agents.idea_generator_agent import idea_generator_agent
from agents.activity_planner_agent import activity_planner_agent
from agents.invitation_writer_agent import invitation_writer_agent
from agents.quality_checker_agent import quality_checker_agent


def main():

    event_name = input("Enter Event Name: ").strip()

    date = input("Enter Event Date: ").strip()

    audience = input("Enter Target Audience: ").strip()

    if not event_name or not date or not audience:
        print("All fields are required.")
        return

    idea_task = create_event_idea_task(
        event_name,
        date,
        audience
    )

    activity_task = create_activity_task(
        event_name,
        idea_task
    )

    invitation_task = create_invitation_task(
        event_name,
        date,
        audience,
        activity_task
    )

    quality_check_task = create_quality_check_task(
        idea_task,
        activity_task,
        invitation_task
    )

    crew = Crew(
        agents=[
            idea_generator_agent,
            activity_planner_agent,
            invitation_writer_agent,
            quality_checker_agent
        ],

        tasks=[
            idea_task,
            activity_task,
            invitation_task,
            quality_check_task
        ],

        process=Process.sequential,
        verbose=True
    )

    crew.kickoff()

    print("\n===== EVENT THEME =====")
    print(idea_task.output.raw)

    print("\n===== ACTIVITIES =====")
    print(activity_task.output.raw)

    print("\n===== INVITATION =====")
    print(invitation_task.output.raw)

    print("\n===== QUALITY CHECK =====")
    print(quality_check_task.output.raw)


if __name__ == "__main__":
    main()