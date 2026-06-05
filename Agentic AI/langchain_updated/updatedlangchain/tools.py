import os
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

model = init_chat_model(model="groq:qwen/qwen3-32b", temperature=0)
print(model)

response = model.invoke(["why do parrots talk?"])
print(response.content, "\n----------------------------------------------------------------")   

# Define tool
@tool
def get_weather(city: str) -> str:
    """Get the weather for a specific city."""
    return f"The weather in {city} is sunny."

# Use the tool
print(get_weather("karachi"))   

model_with_tools = model.bind_tools([get_weather]) 

messages = [{"role":"user", "content":"What's the weather in boston?"}]
ai_msg = model_with_tools.invoke(messages)
messages.append(ai_msg)

for tool_call in ai_msg.tool_calls:
    tool_result = get_weather.invoke(tool_call)
    messages.append(tool_result)

final_response = model_with_tools.invoke(messages)
print(final_response.text, "\n----------------------------------------------------------------") 
