uvicorn quote.app:app --reload --port 3100

docker run -p 3100:3100 --env-file ../../.azure/jong-hello-ai-1/.env quoteapi
