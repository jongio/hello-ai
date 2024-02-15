__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# Path to the marker file
marker_path = "/.data/load_completed.marker"

force_load = os.getenv('FORCE_LOAD', 'false').lower() == 'true'

if not force_load and os.path.exists(marker_path):
    logging.info("Load script has already run; exiting due to marker file presence.")
    sys.exit(0)

logging.info("Loading documents from /files/...")
docs = PyPDFDirectoryLoader("/files/").load()
logging.info(f"Loaded {len(docs)} documents.")

logging.info("Splitting documents into chunks...")
splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=500,
            separators=["\n\n", "\n", " ", ""]
        )
chunks = splitter.split_documents(docs)
logging.info(f"Split into {len(chunks)} chunks.")

logging.info("Generating embeddings...")
embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv('AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME'),
    openai_api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
)

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="/.data"
)
logging.info("Embeddings generated and stored.")

# Create a marker file to prevent rerun on next start
with open(marker_path, 'w') as f:
    f.write('Load script completed')

logging.info("Load script completed successfully.")
