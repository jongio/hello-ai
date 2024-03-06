__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from .base import VectorDB
from langchain_community.vectorstores import Chroma

class ChromaDB(VectorDB):
    def __init__(self, embedding, persist_directory="/.data"):
        self.embedding = embedding
        self.db = Chroma(persist_directory=persist_directory, embedding_function=self.embedding)

    def similarity_search(self, query: str, k: int = 3):
        return self.db.similarity_search(query, k=k)

    @staticmethod
    def from_documents(documents, embedding, persist_directory="/.data"):
        return Chroma.from_documents(
            documents=documents,
            embedding=embedding,
            persist_directory=persist_directory
        )
