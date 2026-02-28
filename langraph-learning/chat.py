from dotenv import load_dotenv

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai",
)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    # print(f"\n\nInside the chatbot node: {state}")
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}


def sample_node(state: State):
    # print(f"\n\nInside the sample node: {state}")
    return {"messages": ["Sample message appended"]}


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sample_node", sample_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sample_node")
graph_builder.add_edge("sample_node", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": ["Hi, My name is harish"]}))
print("\n\nupdated state: ", updated_state)
