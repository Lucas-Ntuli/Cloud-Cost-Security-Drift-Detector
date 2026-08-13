import requests


def generate_markdown_report(drift_findings, policy_findings, cost_estimate):
    """Build a Markdown report summarizing drift, policy, and cost findings."""
    lines = []
    lines.append("# Drift & Security Scan Report")
    lines.append("")

    lines.append("## Drift Findings")
    if not drift_findings:
       lines.append("No drift detected.")
    else:
        for finding in drift_findings:
            lines.append(f"- **{finding.get('type')}** on `{finding.get('resource')}`: "
                          f"{finding.get('message')}")
    lines.append("")

    lines.append("## Policy Findings")
    if not policy_findings:
        lines.append("No policy violations detected.")
    else:
        for finding in policy_findings:
            severity = finding.get("severity", "unknown").upper()
            lines.append(f"- **[{severity}]** `{finding.get('resource')}`: "
                          f"{finding.get('message')}")
    lines.append("")

    lines.append("## Cost Estimate")
    if cost_estimate and cost_estimate.get("estimated_monthly_cost") is not None:
        lines.append(
            f"Estimated monthly cost: "
            f"{cost_estimate['estimated_monthly_cost']} {cost_estimate.get('currency', 'USD')}"
        ) 
    else:
        lines.append("Cost estimate unavailable.")

    return "\n".join(lines)


def write_report(report_text, output_path):
    """Write the report to disk."""
    with open(output_path, "w") as file:
        file.write(report_text)


def send_slack_notification(webhook_url, report_text):
    """Send a summary of the report to Slack, if a webhook URL is configured."""
    if not webhook_url:
        return

    payload = {"text": report_text[:3000]}

    try:
        requests.post(webhook_url, json=payload, timeout=10)
    except requests.RequestException as error:
        print(f"Failed to send Slack notification: {error}")
