import requests

RETAIL_PRICES_API = "https://prices.azure.com/api/retail/prices"


def estimate_storage_account_cost(location="eastus", sku="Standard_LRS"):
    """Look up an approximate monthly cost for a storage account SKU."""
    filter_query = (
        f"serviceName eq 'Storage' and skuName eq '{sku}' "
        f"and armRegionName eq '{location}' and priceType eq 'Consumption'"
    )
    params = {"$filter": filter_query}

    try:
        response = requests.get(RETAIL_PRICES_API, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as error:
        return {"error": str(error), "estimated_monthly_cost": None}

    items = data.get("Items", [])
    if not items:
        return {"estimated_monthly_cost": None, "note": "No pricing data found"}

    unit_price = items[0].get("retailPrice", 0)
    hours_per_month = 730
    estimated_monthly_cost = round(unit_price * hours_per_month, 2)

    return {
        "estimated_monthly_cost": estimated_monthly_cost,
        "currency": items[0].get("currencyCode", "USD"),
        "sku": sku,
        "location": location,
    }
