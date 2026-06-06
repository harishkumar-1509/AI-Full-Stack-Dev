"""
request -> before_agent -> before_model -> tools, model -> after_model -> after_agent -> result
"""
import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

agent=create_agent(
    model="gpt-4o-mini",
    checkpointer=InMemorySaver(),
    middleware=[
        # HumanInTheLoopMiddleware(
        #     interrupt_on={
        #         "send_email_tool":{ # name of the tool
        #             "allowed_decision":["approve","edit","reject"]
        #         },
        #         "read_email_tool":False
        #     }
        # ),
        SummarizationMiddleware(
            model="gpt-4o-mini",
            #trigger=("tokens",550)
            trigger=("messages",10),
            #keep=("tokens",200)
            keep=("messages",4)
        )
    ]
)

# Run with thread id
config={"configurable":{"thread_id":"test-1"}}

questions = [
    "What is 2+2",
    "What is 10*5",
    "what is 100/4",
    "what is 15-7",
    "What is 3*3",
    "What is 4*4"
]

for q in questions:
    response = agent.invoke({"messages":[HumanMessage(content=q)]},config)
    print(f"Messages: {response}")
    print(f"Messages: {len(response['messages'])}")