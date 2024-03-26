import os
from .chroma import ChromaDB
from .azure_search import AzureSearchDB

from langchain_openai import (
    AzureOpenAIEmbeddings,
)


def get_vectordb(embedding=None, persist_directory="/.data"):
    vectordb_type = os.getenv("VECTORDB_TYPE", "azure_search").lower()

    if embedding is None:
        embedding = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )

    if vectordb_type == "chroma":
        return ChromaDB(embedding=embedding, persist_directory=persist_directory)
    elif vectordb_type == "azure_search":
        return AzureSearchDB(
            search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            search_index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
            search_api_key=os.getenv("AZURE_SEARCH_API_KEY"),
            openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            openai_embeddings_deployment_name=os.getenv(
                "AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"
            ),
            openai_embeddings_model_name=os.getenv("AZURE_OPENAI_EMBEDDINGS_MODEL_NAME"),
        )
    else:
        raise ValueError(f"Unsupported vector database type: {vectordb_type}")
