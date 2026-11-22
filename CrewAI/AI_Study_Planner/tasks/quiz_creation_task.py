from crewai import Task
from agents.quiz_creator_agent import quiz_creator_agent

def create_quiz_task(topic, study_plan_task):

    quiz_task = Task(
        description=(
            f"Create a beginner-friendly quiz for the Python topic: {topic}. "
            "Use the study plan prepared by the Study Planner Agent. "
            "Create five easy practice questions. "
            "Questions should be suitable for beginners. "
            "Do not provide answers or solutions."
        ),

        expected_output=(
            "Five beginner-friendly practice questions "
            "without answers."
        ),

        agent=quiz_creator_agent,

        context=[study_plan_task]
    )

    return quiz_task
