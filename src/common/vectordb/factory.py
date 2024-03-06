# src/common/vectordb/factory.py

import os
from .chroma import ChromaDB
from langchain_openai import AzureOpenAIEmbeddings  # Assuming you're using this for embeddings

def get_vectordb(embedding=None, documents=None, persist_directory="/.data"):
    vectordb_type = os.getenv('VECTORDB_TYPE', 'chroma').lower()
    
    if embedding is None:
        # Initialize your default embeddings here, if necessary
        embedding = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv('AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME'),
            openai_api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
        )

    if vectordb_type == 'chroma':
        if documents:
            return ChromaDB.from_documents(documents=documents, embedding=embedding, persist_directory=persist_directory)
        else:
            return ChromaDB(embedding=embedding, persist_directory=persist_directory)
    else:
        raise ValueError(f"Unsupported vector database type: {vectordb_type}")
