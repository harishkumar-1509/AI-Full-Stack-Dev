from dotenv import load_dotenv

from typing_extensions import TypedDict
from typing import Optional, Literal

from langgraph.graph import StateGraph, START, END

from openai import OpenAI

load_dotenv()

client = OpenAI()


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_goo: Optional[bool]


def chatbot(state: State):
    print("\n\nChatbot Node: ", state)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": state.get("user_query"),
            },
        ],
    )

    state["llm_output"] = response.choices[0].message.content
    return state


def evaluate_response(state: State) -> Literal["chatbot_gemini", "end_node"]:
    print("\n\nevaluate Node: ", state)
    if False:
        return "end_node"
    return "chatbot_gemini"


def chatbot_gemini(state: State):
    print("\n\nChatbot Gemini Node: ", state)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": state.get("user_query"),
            },
        ],
    )

    state["llm_output"] = response.choices[0].message.content
    return state


def end_node(state: State):
    print("\n\nEnd Node: ", state)
    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("end_node", end_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)
graph_builder.add_edge("chatbot_gemini", "end_node")
graph_builder.add_edge("end_node", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "Hey, What is 2+2?"}))

print("updated state: ", updated_state)
