import os
from typing_extensions import TypedDict, Annotated
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain.messages import AIMessage
#from dataclass import dataclass

"""
@datatclass
class ContactInfo:
    name: str #The name of the person
    email: str # The email address of the person
    phone: str # The phone number fo the person

use the same agent as below, just replace the response_format with this dataclass
"""

from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class ContactInfo(TypedDict):
    """Contact information of the person"""
    name: str # The name of the person
    email: str # The email address of the person
    phone: str # The phone number fo the person

agent = create_agent(
    model="gpt-5",
    response_format=ContactInfo
)

result = agent.invoke({
    "messages":[{"role":"user", "content":"Extract the contact infor from: John dow, john@gmail.com, 976543210"}]
})

print(result['structured_response'])

class Actor(BaseModel):
    name: str
    role: str

class Movie(BaseModel):
    title: str=Field(description="The title of the movie")
    year: int=Field(description="The release year of the movie")
    genre: str=Field(description="The genre of the movie")
    rating: float=Field(description="The rating of the movie")
    actors: list[Actor]

class MovieDict(TypedDict):
    title: Annotated[str, ...,"The title of the movie"]
    year: Annotated[int, ..., "The year the movie was released"]
    director: Annotated[str, ..., "The director of the movie"]
    rating: Annotated[float, ..., "The movie's rating out of 10"]

model = init_chat_model(model="gpt-4.1", temperature=0)
# can add include_raw=true, display the raw response
#model_with_structure = model.with_structured_output(Movie)
model_with_structure = model.with_structured_output(MovieDict)

response = model_with_structure.invoke(["Provide details about the moview Leo"])
print(response)
print(model.profile)