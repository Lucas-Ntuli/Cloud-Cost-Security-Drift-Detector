FIELDS_TO_COMPARE = [
    "allow_blob_public_access",
    "enable_https_traffic_only",
    "min_tls_version",
]


def compare_storage_accounts(expected_accounts, live_accounts):
    """Compare Terraform-expected vs live Azure storage accounts for drift."""
    drift_findings = []

    expected_by_name = {acc.get("name"): acc for acc in expected_accounts}
    live_by_name = {acc.get("name"): acc for acc in live_accounts}

    for name, expected in expected_by_name.items():
        live = live_by_name.get(name)

        if live is None:
           drift_findings.append({
               "resource": name,
               "type": "missing_in_azure",
               "message": f"Resource '{name}' exists in Terraform but not in Azure.",
        })
        continue

   for field in FIELDS_TO_COMPARE:
       expected_value = expected.get(field)
       live_value = live.get(field)

       if expected_value != live_value:
           drift_findings.append({
               "resource": name,
               "type": "config_drift",
               "field": field,
               "expected": expected_value,
               "actual": live_value,
               "message": (
                  f"Field '{field}' drifted: expected {expected_value}, "
                  f"found {live_value}."
               ),
           })

   for name in live_by_name:
       if name not in expected_by_name:
           drift_findings.append({
               "resource": name,
               "type": "unmanaged_in_azure",
               "message": f"Resource '{name}' exists in Azure but not in Terraform.",
           })

   return drift_findings
