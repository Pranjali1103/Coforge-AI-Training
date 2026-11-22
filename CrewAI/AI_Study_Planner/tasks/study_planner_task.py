from crewai import Task
from agents.study_planner_agent import study_planner_agent

def create_study_plan_task(topic, explanation_task):

    study_plan_task = Task(
        description=(
            f"Create a beginner-friendly 1 week study plan for the Python topic: {topic}. "
            "Use the explanation provided by the Topic Explainer Agent. "
            "Create a study plan from day 1 to Day 7."
            "Keep the plan simple and suitable for beginners. "
            "Include learning goals and practice questions for each day."
        ),

        expected_output=(
            "A structured 7-day study plan containing "
            "Day 1 to Day 7 activities with learning objectives."
        ),

        agent=study_planner_agent,

        context=[explanation_task]
        # Uses the output from Topic Explainer Task
    )

    return study_plan_task