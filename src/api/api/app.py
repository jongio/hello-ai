__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
from fastapi import FastAPI, Request, HTTPException
from openai import AzureOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv()

# Initialize AzureOpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

app = FastAPI()

# Endpoint to generate a random quote
@app.get("/quote")
async def random_quote():
    try:
        completion = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[
                {
                    "role": "user",
                    "content": "Generate a random inspirational quote from a random star wars character and attribute them",
                },
            ],
        )
        return {"quote": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

# Define a Pydantic model for the chat request body
class ChatRequest(BaseModel):
    message: str


system_prompt = "Using only the provided embeddings (E) from the vectordb, find the most relevant answer to the user question (Q). Do not use external knowledge. You will receive data in this format: 'E:{content}\nQ:{question}'"

# Endpoint for chat
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv('AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME'),
            openai_api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
        )
        vectordb = Chroma(persist_directory="/.data", embedding_function=embeddings)
        docs = vectordb.similarity_search(request.message, k=3)
        user_prompt = f"E:{docs}\nQ:{request.message}"
        completion = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],           
            temperature=0.0 
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))