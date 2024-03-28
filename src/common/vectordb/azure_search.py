import logging
from .vectordb import VectorDB
from openai import AzureOpenAI, RateLimitError
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

from tenacity import (
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

# Ensure logging is configured at the start of your application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AzureSearchDB(VectorDB):
    def __init__(
        self,
        search_endpoint,
        search_api_key,
        search_index_name,
        openai_endpoint,
        openai_api_key,
        openai_api_version,
        openai_embeddings_deployment_name,
        openai_embeddings_model_name,
    ):
        logging.info("Initializing AzureSearchDB instance")
        try:
            self.search_endpoint = search_endpoint
            self.search_api_key = search_api_key
            self.search_index_name = search_index_name
            self.openai_endpoint = openai_endpoint
            self.openai_api_key = openai_api_key
            self.openai_api_version = openai_api_version
            self.openai_embeddings_deployment_name = openai_embeddings_deployment_name
            self.openai_embeddings_model_name = openai_embeddings_model_name
            self.search_client = SearchClient(
                self.search_endpoint, self.search_index_name, AzureKeyCredential(self.search_api_key)
            )
            self.index_client = SearchIndexClient(
                self.search_endpoint, AzureKeyCredential(self.search_api_key)
            )
            self.openai_client = AzureOpenAI(
                azure_deployment=self.openai_embeddings_deployment_name,
                api_version=self.openai_api_version,
                azure_endpoint=self.openai_endpoint,
                api_key=self.openai_api_key
            )
            logging.info("AzureSearchDB instance initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize AzureSearchDB instance: {e}")
            raise

    def search(self, query: str, k: int = 3):
        logging.info(f"Performing search for query: {query}")
        try:
            embedding = (
                self.openai_client.embeddings.create(
                    input=query, model=self.openai_embeddings_model_name
                )
                .data[0]
                .embedding
            )
            vector_query = VectorizedQuery(
                vector=embedding, k_nearest_neighbors=k, fields="contentVector"
            )

            results = self.search_client.search(
                search_text=None, vector_queries=[vector_query], select=["content"], include_total_count=True
            )
            logging.info(f"Search completed, found {results.get_count()} results")
            return [result for result in results]
        except Exception as e:
            logging.error(f"Search failed for query: {query}, error: {e}")
            raise

    def create_index(self):
        logging.info(f"Creating index '{self.search_index_name}'")
        try:
            # Define the structure of your index
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
                name=self.search_index_name,
                fields=fields,
                vector_search=vector_search,
                semantic_search=semantic_search,
            )

            # Create the index
            self.index_client.create_or_update_index(index)
            logging.info(f"Index '{self.search_index_name}' created or updated successfully.")
        except Exception as e:
            logging.error(f"Failed to create or update index '{self.search_index_name}': {e}")
            raise

    def prepare_documents(self, documents):
        logging.info("Preparing documents for indexing")
        try:
            docs = []
            for i, doc in enumerate(documents):
                docs.append(
                    {
                        "id": str(i),  # Unique identifier for each chunk
                        "content": doc.page_content,  # Text content of the chunk
                    }
                )
            logging.info(f"Prepared {len(docs)} documents for indexing")
            return docs
        except Exception as e:
            logging.error(f"Error preparing documents for indexing: {e}")
            raise

    def create_embeddings(self, documents):
        logging.info("Creating embeddings for documents")
        try:
            content = [doc["content"] for doc in documents]
            
            for attempt in Retrying(
                retry=retry_if_exception_type(RateLimitError),
                wait=wait_random_exponential(min=15, max=60),
                stop=stop_after_attempt(15),
                before_sleep=self.before_retry_sleep,
            ):
                with attempt:
                    emb_response = self.openai_client.embeddings.create(
                        input=content, model=self.openai_embeddings_model_name
                    )
                    
                    content_embeddings = [item.embedding for item in emb_response.data]

                    for i, doc in enumerate(documents):
                        doc["contentVector"] = content_embeddings[i]
                    
                    logging.info("Embeddings created and assigned to documents successfully")


        except Exception as e:
            logging.error(f"Failed to create embeddings for documents: {e}")
            raise

    def before_retry_sleep(self, retry_state):
        logging.info(f"Retrying after {retry_state.outcome_timestamp} with error: {retry_state.outcome}.")
                     
    def index_documents(self, documents):
        logging.info("Indexing documents")
        try:
            self.create_index()
            docs = self.prepare_documents(documents)
            self.create_embeddings(docs)
            logging.info("Uploading documents to Azure Search...")
            self.search_client.upload_documents(documents=docs)
            logging.info("Documents indexed successfully")
        except Exception as e:
            logging.error(f"Failed to index documents: {e}")
            raise
