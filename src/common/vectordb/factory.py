# src/common/vectordb/factory.py

import os
from .chroma import ChromaDB
from .azure_search import AzureSearchDB  # Assuming azure_search.py is the filename

from langchain_openai import AzureOpenAIEmbeddings  # Assuming you're using this for embeddings

def get_vectordb(embedding=None, persist_directory="/.data"):
    vectordb_type = os.getenv('VECTORDB_TYPE', 'azure_search').lower()
    
    if embedding is None:
        # Initialize your default embeddings here, if necessary
        embedding = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv('AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME'),
            openai_api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
        )

    if vectordb_type == 'chroma':
        return ChromaDB(embedding=embedding, persist_directory=persist_directory)
    elif vectordb_type == 'azure_search':
        # Add your Azure Search specific parameters here
        return AzureSearchDB(
            service_name=os.getenv('AZURE_SEARCH_SERVICE_NAME'),
            index_name=os.getenv('AZURE_SEARCH_INDEX_NAME'),
            api_key=os.getenv('AZURE_SEARCH_API_KEY')
        )
    else:
        raise ValueError(f"Unsupported vector database type: {vectordb_type}")
