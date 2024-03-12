import logging
from .vectordb import VectorDB
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SimpleField,
    SearchFieldDataType,
    SearchableField,
    SearchField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
    SemanticSearch,
    SearchIndex,
)


class AzureSearchDB(VectorDB):
    def __init__(
        self,
        service_name,
        search_api_key,
        index_name,
        embedding_deployment_name,
        embedding_model_name,
        openai_endpoint,
        openai_api_key,
        openai_api_version,
        endpoint_suffix="search.windows.net",
    ):
        self.service_name = service_name
        self.index_name = index_name
        self.search_api_key = search_api_key
        self.openai_endpoint = openai_endpoint
        self.openai_api_version = openai_api_version
        self.openai_api_key = openai_api_key
        self.endpoint_suffix = endpoint_suffix
        self.endpoint = f"https://{self.service_name}.{self.endpoint_suffix}"
        self.embedding_deployment_name = embedding_deployment_name
        self.embedding_model_name = embedding_model_name
        self.search_client = SearchClient(
            self.endpoint, self.index_name, AzureKeyCredential(self.search_api_key)
        )
        self.index_client = SearchIndexClient(
            self.endpoint, AzureKeyCredential(self.search_api_key)
        )

        openai_credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            openai_credential, "https://cognitiveservices.azure.com/.default"
        )

        self.openai_client = AzureOpenAI(
            azure_deployment=self.embedding_deployment_name,
            api_version=self.openai_api_version,
            azure_endpoint=self.openai_endpoint,
            api_key=self.openai_api_key,
            # azure_ad_token_provider=token_provider if not self.openai_api_key else None,
        )

    def search(self, query: str, k: int = 3):
        # Construct your search query and options
        embedding = (
            self.openai_client.embeddings.create(
                input=query, model=self.embedding_model_name
            )
            .data[0]
            .embedding
        )
        vector_query = VectorizedQuery(
            vector=embedding, k_nearest_neighbors=3, fields="contentVector"
        )

        results = self.search_client.search(
            search_text=None, vector_queries=[vector_query], select=["content"]
        )
        return [
            result for result in results
        ]  # Modify as needed based on how you want to process results

    def create_index(self):
        # Define the structure of your index only if necessary
        fields = [
            SimpleField(
                name="id",
                type=SearchFieldDataType.String,
                key=True,
                sortable=True,
                filterable=True,
                facetable=True,
            ),
            SearchableField(
                name="content",
                type=SearchFieldDataType.String,
                filterable=True,
                sortable=False,
                searchable=True,
                facetable=False,
            ),
            SearchField(
                name="contentVector",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=1536,
                vector_search_profile_name="myHnswProfile",
            ),
        ]

        vector_search = VectorSearch(
            algorithms=[HnswAlgorithmConfiguration(name="myHnsw")],
            profiles=[
                VectorSearchProfile(
                    name="myHnswProfile",
                    algorithm_configuration_name="myHnsw",
                )
            ],
        )

        semantic_config = SemanticConfiguration(
            name="my-semantic-config",
            prioritized_fields=SemanticPrioritizedFields(
                content_fields=[SemanticField(field_name="content")],
            ),
        )

        semantic_search = SemanticSearch(configurations=[semantic_config])

        index = SearchIndex(
            name=self.index_name,
            fields=fields,
            vector_search=vector_search,
            semantic_search=semantic_search,
        )

        # Create the index since it doesn't exist
        self.index_client.create_or_update_index(index)
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

    def create_embeddings(self, documents):
        content = [doc["content"] for doc in documents]
        content_response = self.openai_client.embeddings.create(
            input=content, model=self.embedding_model_name
        )
        content_embeddings = [item.embedding for item in content_response.data]

        for i, doc in enumerate(documents):
            doc["contentVector"] = content_embeddings[i]

    def index_documents(self, documents):
        self.create_index()
        docs = self.prepare_documents(documents)
        self.create_embeddings(docs)
        self.search_client.upload_documents(documents=docs)
