def check_storage_public_access(storage_account):
    """Flag storage accounts that allow public/anonymous access to blobs."""
    findings = []
    allow_public = storage_account.get("allow_blob_public_access", False)

    if allow_public:
        findings.append({
            "severity": "critical",
            "resource": storage_account.get("name", "unknown"),
            "check": "storage_public_access",
            "message": "Storage account allows public blob access.",
        })

    return findings


def check_storage_https_only(storage_account):
    """Flag storage accounts that permit plain HTTP traffic.""" 
    findings = []
    https_only = storage_account.get("enable_https_traffic_only", True)

    if not https_only:
        findings.append({
            "severity": "high",
            "resource": storage_account.get("name", "unknown"),
            "check": "storage_https_only",
            "message": "Storage account does not enforce HTTPS-only traffic.",
        })
 
    return findings


def check_storage_min_tls_version(storage_account):
    """Flag storage accounts using an outdated minimum TLS version."""
    findings = []
    min_tls = storage_account.get("min_tls_version", "TLS1_2")

    if min_tls in ("TLS1_0", "TLS1_1"):
        findings.append({
            "severity": "medium",
            "resource": storage_account.get("name", "unknown"),
            "check": "storage_min_tls_version",
            "message": f"Storage account allows outdated TLS version: {min_tls}.",
        })

    return findings


def run_all_checks(storage_account):
    """Run every policy check against a single storage account."""
    findings = []
    findings.extend(check_storage_public_access(storage_account))
    findings.extend(check_storage_https_only(storage_account))
    findings.extend(check_storage_min_tls_version(storage_account))
    return findings
