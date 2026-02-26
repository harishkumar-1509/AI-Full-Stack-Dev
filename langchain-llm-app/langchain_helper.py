import faiss

from openai import OpenAI

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.vectorstores import FAISS

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


embeddings = OpenAIEmbeddings()

video_url = "https://www.youtube.com/watch?v=5MWT_doo68k"


def create_vector_db_from_youtube(video_url: str) -> FAISS:
    loader = YoutubeLoader.from_youtube_url(video_url)
    transcript = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    docs = text_splitter.split_documents(transcript)
    # print(docs, "\n")

    db = FAISS.from_documents(
        docs,
        embeddings,
    )
    return db


def get_response_from_query(db, query, k=4):
    # text-davinci can handle 4097 tokens
    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        # temperature=0.5,
    )
    prompt = PromptTemplate(
        input_variables=["question", "docs"],
        template="""
        You are a helpful youtube assistant that can answer questions about videos based on video transcript.

        Answer the following question: {question}
        By searching the following video transcript: {docs}

        Only use the factual information from the transcript to answer the question

        If you fell like you don't have enough information, say "I don't know"

        Your answer should be detailed.
        """,
    )

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"question": query, "docs": docs_page_content})


if __name__ == "__main__":
    # pet_names = generate_pet_names("dog")
    # print(pet_names)

    # langchain_search_agent()

    query = input("Enter some question about that video:")
    db = create_vector_db_from_youtube(video_url)
    print(
        get_response_from_query(
            db=db,
            query=query,
        )
    )
