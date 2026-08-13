from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
def get_storage_accounts(subscription_id, resource_group):
     """Fetch live storage account properties from azure for comparison."""
     credential = DefaultAzureCredential()
     client = StorageManagementClient(credential, subscription_id)

     accounts = []
     for account in client.storage_accounts.list_by_resource_group(resource_group):
         properties = account.as_dict()

         accounts.append({
             "name": properties.get("name"),
             "allow_blob_public_access": properties.get(
                  "allow_blob_public_access", False
            ),
            "enable_https_traffic_only": properties.get(
                "enable_https_traffic_only", True
            ),
            "min_tls_version": properties.get("minimum_tls_version", "TLS1_2")
         })

    return accounts
