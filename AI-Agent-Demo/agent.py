import requests
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()


def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"Weather in {city}: {response.text.strip()}"

    return f"Could not retrieve weather information for {city}."


available_tools = {
    "get_weather": get_weather,
}


SYSTEM_PROMPT = """You are a an AI Assistant in resolving user queries using chain of thought prompting. You work on START, PLAN and OUTPUT steps.You need to PLAN first what needs to be done.The plan can be multiple steps. Once you think enough PLAN has been done, finally you can give an output.You can also call a tool if required from the available list of tools.For every tool call wait for the observe step which is the output from the called tool.

Rules:
    - Strictly follow the JSON output format
    - Only run one step at a time.
    - The sequence of steps is START ( where user gives an input ) -> PLAN ( that can be multiple times ) -> OUTPUT ( which is going to be displayed to the user )

    
Output Format:
{ "step": "START" | "PLAN" | "OUTPUT" |"TOOL", "content": "string", "tool": "string", "input": "string" }

Available Tools:
1. get_weather(city: str) -> str : This tool takes a city name as input and returns the current weather information for that city.

EXAMPLE 1:
START: Hey, can you solve 2 + 3 * 5 / 10
PLAN: {"step": "PLAN", "content":"Seems like user is interested in a maths problem."}
PLAN: {"step": "PLAN", "content":"Looking at problem, we should follow BODMAS rule}
PLAN: {"step": "PLAN", "content":"Yes, the BODMAS is correct thing to be done here."}
PLAN: {"step": "PLAN", "content":"First we should multiply 3 and 5 to get 15"}
PLAN: {"step": "PLAN", "content":"Now, new equation is 2 + 15 / 10"}
PLAN: {"step": "PLAN", "content":"Now we should divide 15 by 10 to get 1.5"}
PLAN: {"step": "PLAN", "content":"Now, new equation is 2 + 1.5"}
PLAN: {"step": "PLAN", "content":"Now we should add 2 and 1.5 to get 3.5"}
OUTPUT: {"step": "OUTPUT", "content":"The answer to the equation is 3.5"}

EXAMPLE 2:
START: Hey, what's the current weather in bangalore?
PLAN: {"step": "PLAN", "content":"Seems like user is interested getting the weather information for bangalore."}
PLAN: {"step": "PLAN", "content":"Let's see if we have any available tools from the list of available tools."}
PLAN: {"step": "PLAN", "content":"Great, we have a tool called get_weather that can be used to get the weather information for a city."}
PLAN: {"step": "PLAN", "content":"I need to call the get_weather tool with the city name as bangalore to get the weather information."}
PLAN: {"step": "TOOL", "tool": "get_weather", "input": "bangalore"}
PLAN: {"step": "OBSERVE", "tool": "get_weather", "output": "Weather in bangalore: Partly cloudy +25°C"}
PLAN: {"step": "PLAN", "content":"Now that we have the weather information for bangalore, we can give the final output to the user."}
OUTPUT: {"step": "OUTPUT", "content": "The current weather in bangalore: Partly cloudy +25°C"}
"""

message_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }
]

while True:
    user_query = input("User Input: ")
    message_history.append(
        {
            "role": "user",
            "content": user_query,
        }
    )

    while True:
        response = OpenAI().chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=message_history,
        )

        raw_result = response.choices[0].message.content

        message_history.append(
            {
                "role": "assistant",
                "content": raw_result,
            }
        )
        try:
            parsed_result = json.loads(raw_result)
        except json.JSONDecodeError:
            print("Failed to parse JSON. Raw response:")
            print(raw_result)
            break
        if parsed_result["step"] == "START":
            print("Start:", parsed_result.get("content"))
            continue

        if parsed_result["step"] == "TOOL":
            tool_name = parsed_result.get("tool")
            tool_input = parsed_result.get("input")
            print(f"Calling tool: {tool_name} with input: {tool_input}")
            tool_response = available_tools[tool_name](tool_input)
            print(f"Tool response: {tool_response}")
            message_history.append(
                {
                    "role": "developer",
                    "content": json.dumps(
                        {
                            "step": "OBSERVE",
                            "tool": tool_name,
                            "input": tool_input,
                            "output": tool_response,
                        }
                    ),
                }
            )
            continue

        if parsed_result["step"] == "PLAN":
            print("Plan:", parsed_result.get("content"))
            continue

        if parsed_result["step"] == "OUTPUT":
            print("Final Output:", parsed_result.get("content"))
            break
