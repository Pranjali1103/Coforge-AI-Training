from crewai import Crew,Process
from agents.tutor_agent import python_tutor
from agents.assessment_agent import assessment_agent
from tasks.tutor_task import create_tutor_task
from tasks.assessment_task import create_assessment_task



def main():
    print("==========================================")
    print("   MULTI-AGENT AI PYTHON TUTOR    ")
    print("   Powered by CrewAI    ")
    print("==========================================")

    topic=input(
        "Enter Python topic:"
    ).strip()

    if not topic:
        print("Please enter a valid Python topic")
        return

    # Step1:Create the task
    tutor_task=create_tutor_task(topic)

    assessment_task=create_assessment_task(
        topic,
        tutor_task
    )


    # Step 2:Create the crew
    python_crew=Crew(
        agents=[python_tutor,
                assessment_agent],
        tasks=[tutor_task,
               assessment_task],
        process=Process.sequential,
        verbos=True
    )

    # Step 3:Execute the crew
    try:
        result=python_crew.kickoff()
        print("\n=============Python Lesson=================\n")
        print(tutor_task.output.raw)

        print("\n============Python Assessment===============\n")
        print(assessment_task.output.raw)

        print("\n===========FINAL CREW OUTPUT=================\n")
        print(result.raw)


    except Exception as error:
        print("CrewAI execution failed",type(error).__name__)


if __name__=="__main__":
    main()