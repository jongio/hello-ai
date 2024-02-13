import os
from fastapi import FastAPI, Request, HTTPException
from openai import AzureOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

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

# Endpoint for chat
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[
                {"role": "user", "content": request.message},
            ],
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))