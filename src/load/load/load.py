from langchain_community.document_loaders import PyPDFDirectoryLoader
from common.vectordb.factory import get_vectordb
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
import logging
import sys
import time 

def init_logging():
    """Initializes logging."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Logging initialized.")

def load_documents():
    """Loads documents from a specified directory."""
    try:
        logging.info("Loading documents from /files/...")
        docs = PyPDFDirectoryLoader("files").load()
        logging.info(f"Loaded {len(docs)} documents.")
        return docs
    except Exception as e:
        logging.error(f"Failed to load documents: {e}")
        raise

def split_documents(docs):
    """Splits documents into smaller chunks."""
    logging.info("Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, chunk_overlap=500, separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    logging.info(f"Split into {len(chunks)} chunks.")
    return chunks

def index_documents(chunks):
    """Generates embeddings for document chunks."""
    try:
        logging.info("Generating embeddings...")
        embedding = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )
        vectordb = get_vectordb(embedding=embedding, persist_directory="/.data")
        vectordb.index_documents(documents=chunks)
        logging.info("Embeddings generated and stored.")
    except Exception as e:
        logging.error(f"Failed to generate embeddings: {e}")
        raise

def main():
    """Main method to run the script."""
    init_logging()
    try:
        load_dotenv()

        debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        debug_wait_time = int(os.getenv('DEBUG_WAIT_TIME', '0'))

        if debug_mode:
            logging.info(f"Debug mode is enabled. Waiting {debug_wait_time} seconds for debugger to attach...")
            time.sleep(debug_wait_time)

        docs = load_documents()
        chunks = split_documents(docs)
        index_documents(chunks)
        logging.info("Load script completed successfully.")
    except Exception as e:
        logging.error(f"Script execution failed: {e}")
        raise

if __name__ == "__main__":
    main()
