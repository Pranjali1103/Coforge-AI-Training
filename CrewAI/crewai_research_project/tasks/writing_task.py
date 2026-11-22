from crewai import Task
from agents.writer_agent import writer_agent

def do_writing_task(topic,research_task):

    writing_task=Task(
        description=(
          f"Write the content for {topic} in such a way that its easy to read for all the beginners and advanced people.Write all the researched data in a well strcutured manner"
        ),
        expected_output=(
           "Write the content in a well structured manner with sumamry and insights"
        ),
        agent=writer_agent,
        context=[research_task]
    )

    return writing_task