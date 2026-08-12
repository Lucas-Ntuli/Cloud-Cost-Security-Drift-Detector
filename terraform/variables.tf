variable "resource_group_name" {
  description = "Name of the resource group that holds the watched infrastructure"
  type        = string
  default     = "drift-detector-rg"
}

variable "location" {
  description = "Azure region to deploy resources into"
  type        = string
  default     = "westeurope"
}
