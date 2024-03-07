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


def check_marker_file(marker_path):
    """Checks for the presence of a marker file."""
    force_load = os.getenv("FORCE_LOAD", "false").lower() == "true"
    if not force_load and os.path.exists(marker_path):
        logging.info(
            "Load script has already run; exiting due to marker file presence."
        )
        sys.exit(0)


def load_documents():
    """Loads documents from a specified directory."""
    logging.info("Loading documents from /files/...")
    docs = PyPDFDirectoryLoader("/files/").load()
    logging.info(f"Loaded {len(docs)} documents.")
    return docs


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
    logging.info("Generating embeddings...")
    embedding = AzureOpenAIEmbeddings(
        azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )
    vectordb = get_vectordb(embedding=embedding, persist_directory="/.data")
    vectordb.index_documents(documents=chunks)
    logging.info("Embeddings generated and stored.")


def create_marker_file(marker_path):
    """Creates a marker file to indicate completion."""
    with open(marker_path, "w") as f:
        f.write("Load script completed")


def main():
    """Main method to run the script."""
    load_dotenv()
    marker_path = "/.data/load_completed.marker"
    init_logging()
    check_marker_file(marker_path)

    # Check if debug mode is enabled and if we should wait for the debugger to attach
    debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    debug_wait_time = int(os.getenv('DEBUG_WAIT_TIME', '0'))

    if debug_mode and debug_wait_time > 0:
        logging.info(f"Debug mode is enabled. Waiting {debug_wait_time} seconds for debugger to attach...")
        time.sleep(debug_wait_time)

    # Continue with the script execution
    docs = load_documents()
    chunks = split_documents(docs)
    index_documents(chunks)
    create_marker_file(marker_path)
    logging.info("Load script completed successfully.")


# Check if the script is being run directly
if __name__ == "__main__":
    main()
