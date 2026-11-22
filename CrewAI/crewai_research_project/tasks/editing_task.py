from crewai import Task
from agents.editor_agent import editor_agent

def do_editing_task(topic,writing_task):
    editing_task=Task(
        description=(
            f"Edit the content in such a way that all the errors are gone and its easy to read"
        ),
        expected_output=(
          "Edit the content and make it more interesting to read without changing the original research data"
        ),
        agent=editor_agent,
        context=[writing_task]
    )
    return editing_task