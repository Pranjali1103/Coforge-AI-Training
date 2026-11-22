from agents.hospital_agent import create_hospital_agent
agent = create_hospital_agent()

def process_request(message: str):

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
    )

    return response

from models.response_model import HospitalResponse

def process_request(message: str, user_role: str):

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Role: {user_role}\nMessage: {message}"
                }
            ]
        }
    )

    ai_message = result["messages"][-1].content

    return HospitalResponse(
        status="success",
        response=ai_message,
        tools_used=[],
        data={}
    )
