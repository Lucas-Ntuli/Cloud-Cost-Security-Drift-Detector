terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstatedriftdetector01"
    container_name       = "tfstate"
    key                  = "drift-detector.tfstate"
  }
}

provider "azurerm" {
  features {} 
}