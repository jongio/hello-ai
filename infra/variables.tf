variable "location" {
  type = string
}

variable "environment_name" {
  description = "The name of the azd environment to be deployed"
  type        = string
}

variable "principal_id" {
  description = "The Id of the azd service principal to add to deployed keyvault access policies"
  type        = string
  default     = ""
}

variable "workspace" {
  description = "value of workspace"
  type        = string
  default     = "dev"
}

variable "openai_model_name" {
  description = "value of azure openai model name"
  type        = string
  default     = "gpt-35-turbo"
}

variable "openai_model_version" {
  description = "value of azure openai model version"
  type        = string
  default     = "0914"
}

variable "openai_model_capacity" {
  description = "value of azure openai model capacity"
  type        = number
  default     = 120
}

variable "k8s_namespace" {
  description = "value of kubernetes namespace"
  type        = string
  default     = "default"
}
