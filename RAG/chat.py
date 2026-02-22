from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="pdf-documents",
    embedding=embedding_model,
)

# Take user input
user_query = input("Enter your query: ")

# Relevant chunks from vector db
search_results = vector_db.similarity_search(
    query=user_query,
)

# print(search_results)

context = "\n\n\n".join(
    [
        f"Page Number: {result.metadata['page']}\nContent: {result.page_content}\nFile Location: {result.metadata['source']}"
        for result in search_results
    ]
)
# print(f"Context retrieved from vector database:\n{context[0:10]}")
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
            "content": user_query,
        },
    ],
)

print(f"🤖: {openai_response.choices[0].message.content}")
