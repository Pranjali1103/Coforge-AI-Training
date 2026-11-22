from crewai import Crew,Process

from tasks.editing_task import do_editing_task
from tasks.researcher_tasks import do_reasearch_task
from tasks.writing_task import do_writing_task

from agents.editor_agent import editor_agent
from agents.writer_agent import writer_agent
from agents.researcher_agent import research_agent

def main():

    print("==========================================")
    print("   Research Data:   ")
    print("   Powered by CrewAI    ")
    print("==========================================")

    topic = input("Enter research topic: ").strip()

    if not topic:
        print("Topic cannot be empty.")
        return

    research_task=do_reasearch_task(topic)

    writing_task=do_writing_task(topic,research_task)

    editing_task=do_editing_task(topic,writing_task)

    crew=Crew(
        agents=[
           research_agent,
           writer_agent,
           editor_agent
        ],
        tasks=[
          research_task,
          writing_task,
          editing_task
        ],
        process=Process.sequential,
        verbose=True

    )

    result = crew.kickoff()
    print(research_task.output.raw)
    print(writing_task.output.raw)
    print(editing_task.output.raw)


if __name__ == "__main__":
    main()