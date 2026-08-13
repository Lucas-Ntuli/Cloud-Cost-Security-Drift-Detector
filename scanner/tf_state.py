import json


def load_terraform_state(state_path):
    """Load and parse a Terraform state JSON file."""
    with open(state_path, "r") as file:
         return json.load(file)


def extract_storage_accounts(tf_state):
    """Pull expected storage account resources out of Terraform state."""
    accounts = []

    root_module = tf_state.get("values", {}).get("root_module", {})
    resources = root_module.get("resources", [])

    for resource in resources:
        if resource.get("type") == "azurerm_storage_account":
            values = resource.get("values", {})
            accounts.append({
                "name": values.get("name"),
                "allow_blob_public_access": values.get(
                    "allow_nested_items_to_be_public", False
                ),
                "enable_https_traffic_only": values.get(
                    "enable_https_traffic_only", True
                ),
                "min_tls_version": values.get("min_tls_version", "TLS1_2"),
            })

    return accounts
