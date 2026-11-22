from crewai import Crew, Process

from tasks.explanation_task import create_explanation_task
from tasks.study_planner_task import create_study_plan_task
from tasks.quiz_creation_task import create_quiz_task

from agents.topic_explainer_agent import topic_explainer_agent
from agents.study_planner_agent import study_planner_agent
from agents.quiz_creator_agent import quiz_creator_agent


def main():

    print("==========================================")
    print("   THREE-AGENT AI STUDY PLANNER    ")
    print("   Powered by CrewAI    ")
    print("==========================================")

    topic = input("Enter Python topic: ").strip()

    if not topic:
        print("Topic cannot be empty.")
        return

    explanation_task = create_explanation_task(topic)

    study_plan_task = create_study_plan_task(
        topic,
        explanation_task
    )

    quiz_task = create_quiz_task(
        topic,
        study_plan_task
    )

    crew = Crew(
        agents=[
            topic_explainer_agent,
            study_planner_agent,
            quiz_creator_agent
        ],

        tasks=[
            explanation_task,
            study_plan_task,
            quiz_task
        ],

        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    print(explanation_task.output.raw)
    print(study_plan_task.output.raw)
    print(quiz_task.output.raw)


if __name__ == "__main__":
    main()