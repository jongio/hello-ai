from .vectordb import VectorDB
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchFieldDataType, SearchableField
import logging


class AzureSearchDB(VectorDB):
    def __init__(
        self, service_name, index_name, api_key, endpoint_suffix="search.windows.net"
    ):
        self.service_name = service_name
        self.index_name = index_name
        self.api_key = api_key
        self.endpoint_suffix = endpoint_suffix
        self.endpoint = f"https://{self.service_name}.{self.endpoint_suffix}"
        self.client = SearchClient(
            self.endpoint, self.index_name, AzureKeyCredential(self.api_key)
        )
        self.index_client = SearchIndexClient(
            self.endpoint, AzureKeyCredential(self.api_key)
        )

    def search(self, query: str, k: int = 3):
        # Construct your search query and options
        results = self.client.search(search_text=query, top=k)
        return [
            result for result in results
        ]  # Modify as needed based on how you want to process results

    def create_index(self):
        # Check if the index already exists
        try:
            self.index_client.get_index(self.index_name)
            logging.info(f"Index '{self.index_name}' already exists.")
        except Exception as e:
            # The index does not exist, so define its structure and create it
            logging.info(f"Index '{self.index_name}' does not exist. Creating...")

            # Define the structure of your index only if necessary
            fields = [
                SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True),
                SearchableField(
                    name="content",
                    type=SearchFieldDataType.String,
                    filterable=True,
                    sortable=False,
                    searchable=True,
                    facetable=False,
                ),
                # Add more fields here based on your requirements.
            ]
            index = SearchIndex(name=self.index_name, fields=fields)

            # Create the index since it doesn't exist
            self.index_client.create_index(index)
            logging.info(f"Index '{self.index_name}' created.")

    def prepare_documents(self, documents):
        """Converts text chunks into a format suitable for Azure Search indexing."""
        docs = []
        for i, doc in enumerate(documents):
            # Each chunk becomes a document; adjust 'id' and 'content' based on your Azure Search index schema
            docs.append(
                {
                    "id": str(i),  # Unique identifier for each chunk
                    "content": doc.page_content,  # Text content of the chunk
                }
            )
        return docs

    def index_documents(self, documents):
        self.create_index()
        docs = self.prepare_documents(documents)
        self.client.upload_documents(documents=docs)
