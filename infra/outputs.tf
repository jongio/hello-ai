output "AZURE_AKS_CLUSTER_NAME" {
  value = local.is_default_workspace ? "" : azurerm_kubernetes_cluster.aks[0].name
}

output "AZURE_AKS_IDENTITY_CLIENT_ID" {
  value = local.is_default_workspace ? "" : azurerm_kubernetes_cluster.aks[0].kubelet_identity[0].object_id
}

output "AZURE_AKS_NAMESPACE" {
  value = local.is_default_workspace ? "" : var.k8s_namespace
}

output "AZURE_CONTAINER_REGISTRY_ENDPOINT" {
  value = local.is_default_workspace ? "" : azurerm_container_registry.acr[0].login_server
}

output "AZURE_CONTAINER_REGISTRY_NAME" {
  value = local.is_default_workspace ? "" : azurerm_container_registry.acr[0].name
}

output "AZURE_LOCATION" {
  value = local.location
}

output "AZURE_OPENAI_API_KEY" {
  value     = azurerm_cognitive_account.cog.primary_access_key
  sensitive = true
}

output "AZURE_OPENAI_API_VERSION" {
  value = var.openai_api_version
}

output "AZURE_OPENAI_DEPLOYMENT_NAME" {
  value = var.openai_deployment_name
}

output "AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME" {
  value = var.openai_embeddings_deployment_name
}

output "AZURE_OPENAI_EMBEDDINGS_MODEL_NAME" {
  value = var.openai_embeddings_model_name
}

output "AZURE_OPENAI_EMBEDDINGS_MODEL_VERSION" {
  value = var.openai_embeddings_model_version
}

output "AZURE_OPENAI_ENDPOINT" {
  value = azurerm_cognitive_account.cog.endpoint
}

output "AZURE_OPENAI_MODEL_CAPACITY" {
  value = var.openai_model_capacity
}

output "AZURE_OPENAI_MODEL_NAME" {
  value = var.openai_model_name
}

output "AZURE_OPENAI_MODEL_VERSION" {
  value = var.openai_model_version
}

output "AZURE_RESOURCE_GROUP" {
  value = azurerm_resource_group.rg.name
}

output "AZURE_SEARCH_API_KEY" {
  value     = azurerm_search_service.search.primary_key
  sensitive = true
}

output "AZURE_SEARCH_ENDPOINT" {
  value = "https://${azurerm_search_service.search.name}.search.windows.net"
}

output "AZURE_SEARCH_INDEX_NAME" {
  value = var.search_index_name
}

output "AZURE_SEARCH_SEMANTIC_SKU_NAME" {
  value = var.search_semantic_sku_name
}

output "AZURE_SEARCH_SKU_NAME" {
  value = var.search_sku_name
}

output "AZURE_SKU_NAME" {
  value = var.openai_sku_name
}

output "AZURE_TENANT_ID" {
  value = data.azurerm_client_config.current.tenant_id
}

output "VECTORDB_TYPE" {
  value = var.vectordb_type
}
