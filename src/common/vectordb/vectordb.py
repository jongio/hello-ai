from abc import ABC, abstractmethod

class VectorDB(ABC):

    @abstractmethod
    def search(self, query: str, k: int = 3):
        """
        Perform a similarity search against the vector database.

        :param query: The query string or vector.
        :param k: The number of similar items to retrieve.
        :return: A list of similar items.
        """
        pass

    @abstractmethod
    def index_documents(self, documents):
        """
        Indexes a batch of documents in the vector database.

        :param documents: A list of documents to index. Each document should
                          be a dictionary representing document fields.
        """
        pass
