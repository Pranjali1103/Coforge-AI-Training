from crewai import Task
from agents.topic_explainer_agent import topic_explainer_agent

def create_explanation_task(topic):

    explanation_task = Task(
        description=(
            f"Create an explanation for the Python topic: {topic}. "
            "Explain the topic in a simple and beginner-friendly manner. "
            "Include one small example."
        ),

        expected_output=(
            "The topic should be explained in a well-structured, "
            "easy-to-understand, and beginner-friendly manner with one example."
        ),

        agent=topic_explainer_agent
    )

    return explanation_task