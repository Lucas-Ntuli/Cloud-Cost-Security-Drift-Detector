output "resource_group_name" {
  description = "The name of the resource group created"
  value       = azurerm_resource_group.main.name
}

output "storage_account_name" {
  description = "The name of the storage account created"
  value       = azurerm_storage_account.watched.name
}
