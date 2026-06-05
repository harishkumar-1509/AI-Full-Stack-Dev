import os
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain.messages import AIMessage

from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class Actor(BaseModel):
    name: str
    role: str

class Movie(BaseModel):
    title: str=Field(description="The title of the movie")
    year: int=Field(description="The release year of the movie")
    genre: str=Field(description="The genre of the movie")
    rating: float=Field(description="The rating of the movie")
    actors: list[Actor]

model = init_chat_model(model="gpt-4.1", temperature=0)
# can add include_raw=true, display the raw response
model_with_structure = model.with_structured_output(Movie)

response = model_with_structure.invoke(["Provide details about the moview Inception"])
print(response)