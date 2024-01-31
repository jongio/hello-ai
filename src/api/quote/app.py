import os
from fastapi import FastAPI, Request
from openai import AzureOpenAI
from dotenv import load_dotenv

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
@app.get("/")
async def random_quote():
    try:
        completion = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[
                {
                    "role": "user",
                    "content": "Generate a random inspirational quote that Satya Nadella would say",
                },
            ],
        )
        return {"quote": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
