__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from .vectordb import VectorDB
from langchain_community.vectorstores import Chroma

class ChromaDB(VectorDB):
    def __init__(self, embedding, persist_directory="/.data"):
        self._db = None
        self.embedding = embedding
        self.persist_directory = persist_directory
    
    @property
    def db(self):
        if self._db is None:
            self._db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embedding)
        return self._db
    
    def search(self, query: str, k: int = 3):
        return self.db.similarity_search(query, k=k)

    def index_documents(self, documents):
        return Chroma.from_documents(
            documents=documents,
            embedding=self.embedding,
            persist_directory=self.persist_directory
        )
   
