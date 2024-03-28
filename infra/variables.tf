variable "environment_name" {
  description = "Specifies the name of the environment to be deployed."
  type        = string
}

variable "k8s_namespace" {
  description = "Specifies the value of the Kubernetes namespace."
  type        = string
  default     = "default"
}

variable "location" {
  description = "Specifies the location."
  type        = string
}

variable "openai_api_version" {
  description = "Specifies the version of the OpenAI API."
  type        = string
  default     = "2024-03-01-preview"
}

variable "openai_deployment_name" {
  description = "Specifies the name of the deployment for OpenAI."
  type        = string
  default     = "gpt-35-turbo"
}

variable "openai_embeddings_deployment_name" {
  description = "Specifies the name of the deployment for OpenAI embeddings."
  type        = string
  default     = "text-embedding-ada-002"
}

variable "openai_embeddings_model_capacity" {
  description = "Specifies the capacity of the model for OpenAI embeddings."
  type        = number
  default     = 50
}

variable "openai_embeddings_model_name" {
  description = "Specifies the name of the model for OpenAI embeddings."
  type        = string
  default     = "text-embedding-ada-002"
}

variable "openai_embeddings_model_version" {
  description = "Specifies the version of the model for OpenAI embeddings."
  type        = string
  default     = "2"
}

variable "openai_model_capacity" {
  description = "Specifies the capacity of the model for OpenAI."
  type        = number
  default     = 30
}

variable "openai_model_name" {
  description = "Specifies the name of the model for OpenAI."
  type        = string
  default     = "gpt-35-turbo"
}

variable "openai_model_version" {
  description = "Specifies the version of the model for OpenAI."
  type        = string
  default     = "0613"
}

variable "openai_sku_name" {
  description = "Specifies the SKU name for OpenAI."
  type        = string
  default     = "S0"
}

variable "principal_id" {
  description = "Specifies the ID of the service principal to add to deployed KeyVault access policies."
  type        = string
  default     = ""
}

variable "search_index_name" {
  description = "Specifies the name of the search index."
  type        = string
  default     = "docs"
}

variable "search_semantic_sku_name" {
  description = "Specifies the SKU name for semantic search."
  type        = string
  default     = "free"
}

variable "search_sku_name" {
  description = "Specifies the SKU name for search."
  type        = string
  default     = "basic"
}

variable "acr_sku_name" {
  description = "Specifies the SKU name for Azure container registry."
  type        = string
  default     = "Premium"
}

variable "vectordb_type" {
  description = "Specifies the type of vectordb."
  type        = string
  default     = "azure_search"
}

variable "workspace" {
  description = "Specifies the value of the workspace."
  type        = string
  default     = "dev"
}
