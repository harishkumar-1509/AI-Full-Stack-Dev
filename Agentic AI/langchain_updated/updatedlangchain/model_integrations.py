import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")
#os.environ["ANTHROPIC_API_KEY"]=os.getenv("ANTHROPIC_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

model = init_chat_model(model="gpt-4.1", temperature=0)
#print(model)

#call the model

response = model.invoke(["Hello, how are you?"])
print(response.content,"\n----------------------------------------------------------------")

# Google gemini model integration
google_model = init_chat_model(model="google_genai:gemini-2.5-flash-lite", temperature=0)
#print(google_model)

google_response = google_model.invoke(["Hello, how are you?"])
print(google_response.content,"\n----------------------------------------------------------------")

## ChatOpenAI
print("Open AI ChatModel")
openai_model = ChatOpenAI(model="gpt-4.1", temperature=0)
openai_response = openai_model.invoke(["Hello, how are you?"])
print(openai_response.content,"\n----------------------------------------------------------------")

## GROQ Model Integration
print("GROQ ChatModel")
groq_model = init_chat_model(model="groq:qwen/qwen3-32b", temperature=0)
groq_response = groq_model.invoke(["Hello, how are you?"])
print(groq_response.content,"\n---------------------------------------------------------------- ")

# Streaming 
### Streams in Chunks
print("Streaming")
for chunk in model.stream(["Write a 200 words paragraph on artificial intelligence"]):
    print(chunk.text, end=" ", flush=True)    
print("\n----------------------------------------------------------------")

# Batch Processing
print("Batch Processing")
batch = model.batch([["Hello, how are you?"], ["Write a 200 words paragraph on artificial intelligence"]])
for response in batch:
    print(response.content,"\n----------------------------------------------------------------")    

# Async model call
async def main():
    response = await model.ainvoke(["Hello, how are you?"])
    print(response.content,"\n----------------------------------------------------------------")    
    async for chunk in model.astream(["Hello, how are you?"]):        
        print(chunk.text, end=" ", flush=True)   
    print("\n----------------------------------------------------------------")   

import asyncio

asyncio.run(main())