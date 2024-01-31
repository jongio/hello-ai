resource "azurecaf_name" "cog_name" {
  name          = local.resource_token
  resource_type = "azurerm_cognitive_account"
  random_length = 0
  clean_input   = true
}

resource "azurerm_cognitive_account" "cog" {
  name                  = azurecaf_name.cog_name.result
  location              = var.location
  resource_group_name   = azurerm_resource_group.rg.name
  kind                  = "OpenAI"
  sku_name              = "S0"
  custom_subdomain_name = azurecaf_name.cog_name.result
  tags                  = azurerm_resource_group.rg.tags
}

resource "azurerm_cognitive_deployment" "deployment" {
  name                 = var.openai_model_name
  cognitive_account_id = azurerm_cognitive_account.cog.id

  model {
    format  = "OpenAI"
    name    = var.openai_model_name
    version = var.openai_model_version
  }

  scale {
    type     = "Standard"
    capacity = var.openai_model_capacity
  }
}

resource "azurerm_user_assigned_identity" "uai" {
  location            = var.location
  name                = azurecaf_name.cog_name.result
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_federated_identity_credential" "fic" {
  count               = local.is_default_workspace ? 0 : 1
  name                = azurecaf_name.cog_name.result
  resource_group_name = azurerm_resource_group.rg.name
  parent_id           = azurerm_user_assigned_identity.uai.id
  audience            = ["api://AzureADTokenExchange"]
  issuer              = azurerm_kubernetes_cluster.aks[0].oidc_issuer_url
  subject             = "system:serviceaccount:${var.k8s_namespace}:ai-service-account"
}

resource "azurerm_role_assignment" "role_me" {
  principal_id         = data.azurerm_client_config.current.object_id
  role_definition_name = "Cognitive Services OpenAI User"
  scope                = azurerm_cognitive_account.cog.id
}

resource "azurerm_role_assignment" "role_mi" {
  principal_id         = azurerm_user_assigned_identity.uai.principal_id
  role_definition_name = "Cognitive Services OpenAI User"
  scope                = azurerm_cognitive_account.cog.id
}
