from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore


openai_client = OpenAI()

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="pdf-documents",
)


def process_query(query: str):
    print("Searching Chunks", query)
    search_results = vector_store.similarity_search(
        query=query,
    )

    context = "\n\n\n".join(
        [
            f"Page Number: {result.metadata['page']}\nContent: {result.page_content}\nFile Location: {result.metadata['source']}"
            for result in search_results
        ]
    )

    SYSTEM_PROMPT = f"""
    You are a helpful assistant that answers questions based on the available context retrieved from a PDF document along with page content and page number.

    You should only answer the user based on the following context  and navigate the user to open the right page number to know more.

    Context:
    {context}
    """

    openai_response = openai_client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": query,
            },
        ],
    )

    print(f"🤖: {openai_response.choices[0].message.content}")
    return openai_response.choices[0].message.content
