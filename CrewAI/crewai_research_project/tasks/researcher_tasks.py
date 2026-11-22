from crewai import Task
from agents.researcher_agent import research_agent

def do_reasearch_task(topic):

    research_task=Task(
        description=(
          f"Do research for the topic :{topic}.Do research in such a way that all the answers are received "
        ),
        expected_output=(
            "The research must be done in such a way that meaningful data is obtained"
        ),
        agent=research_agent
    )
    return research_task
