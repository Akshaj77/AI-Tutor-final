import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import requests 
import os
from multi_tool_agent.sub_agents.physics_agent import physicsAgent
from multi_tool_agent.sub_agents.math_agent import mathsAgent

def call_gemini_llm(prompt: str) -> str:
    """Calls the Gemini LLM with the provided prompt.

    Args:
        prompt (str): The prompt to send to the Gemini LLM.

    Returns:
        str: The response from the Gemini LLM.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Authorization": f"Bearer {os.getenv("GOOGLE_API_KEY")}",
        "Content-Type": "application/json",
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    # Extract the relevant part of the response
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def get_sub_agent_type(prompt: str) -> dict:
    """Retrieves the sub agent type from the query using Gemini LLM."""
    try:
        # Compose a prompt for the LLM to classify the query
        llm_prompt = (
            "Classify the following query as either 'physics' or 'maths':\n"
            f"Query: {prompt}\n"
            "Respond with only one word: 'physics' or 'maths'."
        )
        llm_response = call_gemini_llm(llm_prompt).strip().lower()
        if llm_response in ["physics", "maths"]:
            return {
                "status": "success",
                "sub_agent": llm_response,
                "report": f"This query should be handled by the {llm_response} sub agent.",
            }
        else:
            return {
                "status": "error",
                "error_message": f"LLM returned an unexpected response: {llm_response}",
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to classify query: {str(e)}",
        }
# def get_current_time(city: str) -> dict:
#     """Returns the current time in a specified city.

#     Args:
#         city (str): The name of the city for which to retrieve the current time.

#     Returns:
#         dict: status and result or error msg.
#     """

#     if city.lower() == "new york":
#         tz_identifier = "America/New_York"
#     else:
#         return {
#             "status": "error",
#             "error_message": (
#                 f"Sorry, I don't have timezone information for {city}."
#             ),
#         }

#     tz = ZoneInfo(tz_identifier)
#     now = datetime.datetime.now(tz)
#     report = (
#         f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
#     )
#     return {"status": "success", "report": report}


root_agent = None
runner_root = None

if physicsAgent and mathsAgent and 'get_sub_agent_type' in globals():
    

    root_agent = Agent(
        name="main_agent",
        model="gemini-2.0-flash",
        description=(
            "The main coordinator agent that delegates tasks to sub-agents based on the type of query. "
        ),
        instruction=(
          "You are the main coordinator agent that delegates tasks to specialized sub-agents. "
        "You have two specialized sub-agents: "
        "1. 'MathsAgent': Handles mathematics-related queries. "
        "2. 'PhysicsAgent': Handles physics-related queries. "
        
        # "First, analyze the user's query using the 'get_sub_agent_type' tool to determine which sub-agent should handle it. "
        "delegate the query to the appropriate sub-agent. "
        # "If the tool returns an error or cannot classify the query, respond that you're unable to handle the request."
        ),
        # tools=[get_sub_agent_type],
        sub_agents=[
             physicsAgent,
             mathsAgent,
        ],
    )