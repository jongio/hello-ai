# src/common/vectordb/base.py

from abc import ABC, abstractmethod

class VectorDB(ABC):
    @abstractmethod
    def similarity_search(self, query: str, k: int = 3):
        """
        Perform a similarity search against the vector database.

        :param query: The query string or vector.
        :param k: The number of similar items to retrieve.
        :return: A list of similar items.
        """
        pass
