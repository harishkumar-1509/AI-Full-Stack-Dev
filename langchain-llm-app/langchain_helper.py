from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_agent


from dotenv import load_dotenv

load_dotenv()


def generate_pet_names(animal_type: str, pet_color: str = "brown") -> str:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    prompt_template_name = PromptTemplate(
        input_variables=["animal_type", "pet_color"],
        template="I have a {animal_type} and I need some cool names for it. Suggest me 5 cool names for my pet with the color {pet_color}.",
    )
    name_chain = prompt_template_name | llm | StrOutputParser()
    return name_chain.invoke({"animal_type": animal_type, "pet_color": pet_color})


def langchain_search_agent():

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        # temperature=0.5,
    )

    search_tool = DuckDuckGoSearchRun()

    agent = create_agent(
        llm,
        [search_tool],
        system_prompt="""
        You are a helpful assistant.
        Use the DuckDuckGoSearchRun tool whenever the question
        requires real-time or factual web information.
        """,
    )

    while True:
        user_query = input("\nAsk something (type 'exit' to quit): ")

        if user_query.lower() == "exit":
            break

        result = agent.invoke({"messages": [{"role": "user", "content": user_query}]})

        print("\n🤖", result["messages"][-1].content)


if __name__ == "__main__":
    # pet_names = generate_pet_names("dog")
    # print(pet_names)
    langchain_search_agent()
