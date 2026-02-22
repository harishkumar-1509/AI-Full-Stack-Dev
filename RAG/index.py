from dotenv import load_dotenv

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

pdf_path = Path(__file__).parent / "python.pdf"

# Load the PDF document into the python program
loader = PyPDFLoader(file_path=str(pdf_path))

# Get the pages of the PDF document as a list of documents
docs = loader.load()

# Split the documents into smaller chunks of text

# The chunk overlap is the number of characters that will be repeated in each chunk. This is useful for ensuring that the chunks are not too small and that they contain enough context for the language model to understand the content of the document.
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(docs)

# Vector Embedding
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="pdf-documents",
)

print("Indexing of PDF document completed!")
