import requests

RETAIL_PRICES_API = "https://prices.azure.com/api/retail/prices"


def estimate_storage_account_cost(location="eastus", sku="Standard_LRS"):
    """Look up an approximate monthly cost for a storage account SKU."""
    filter_query = (
        f"serviceName eq 'Storage' and armRegionName eq '{location}' "
        f"and priceType eq 'Consumption'"
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

    # Normalize for comparison: ignore case and separators (_ / space)
    def normalize(text):
        return text.replace("_", "").replace(" ", "").lower()

    normalized_target = normalize(sku)
    matches = [
        item for item in items
        if normalize(item.get("skuName", "")) == normalized_target
    ]

    candidates = matches if matches else items

    # Prefer the base storage capacity meter over transactions/bandwidth meters
    preferred = [
        item for item in candidates
        if "data stored" in item.get("meterName", "").lower()
    ]
    selected = preferred[0] if preferred else candidates[0]

    unit_price = selected.get("retailPrice", 0)
    unit_of_measure = selected.get("unitOfMeasure", "")

    # NOTE: Storage pricing is typically per GB/month, not per hour.
    # Multiplying by hours_per_month is only correct if unitOfMeasure is hourly.
    if "hour" in unit_of_measure.lower():
        estimated_monthly_cost = round(unit_price * 730, 2)
    else:
        estimated_monthly_cost = round(unit_price, 2)

    return {
        "estimated_monthly_cost": estimated_monthly_cost,
        "currency": selected.get("currencyCode", "USD"),
        "sku": sku,
        "location": location,
        "unit_of_measure": unit_of_measure,
        "matched_sku_name": selected.get("skuName"),
    }