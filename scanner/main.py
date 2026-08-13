import sys
from config import Config
from tf_state import load_terraform_state, extract_storage_accounts
from azure_client import get_storage_accounts
from drift import compare_storage_accounts
from policies import run_all_checks
from cost import estimate_storage_account_cost
from report import generate_markdown_report, write_report, send_slack_notification

def main():
    """Orchestrate the drift detection, policy checks, cost estimate, and report."""
    try:
        Config.validate()
    except EnvironmentError as error:
        print(f"Configuration error: {error}")
        sys.exit(1)
        
   tf_state = load_terraform_state(Config.TF_STATE_PATH)
   expected_accounts = extract_storage_accounts(tf_state)
   live_accounts = get_storage_accounts(
       Config.AZURE_SUBSCRIPTION_ID, Config.TARGET_RESOURCE_GROUP
   )
   
  drift_findings = compare_storage_accounts(expected_accounts, live_accounts)

  policy_findings = []
  for account in live_accounts:
      policy_findings.extend(run_all_checks(account))

  cost_estimate = estimate_storage_account_cost()

  report_text = generate_markdown_report(
      drift_findings, policy_findings, cost_estimate
  )
  write_report(report_text, Config.REPORT_OUTPUT_PATH)
  send_slack_notification(Config.SLACK_WEBHOOK_URL, report_text)

  print(report_text)

  critical_findings = [
      finding for finding in policy_findings
      if finding.get("severity") == "critical"
  ]
  if critical_findings or drift_findings:
     sys.exit(1)

if __name__ == "__main__":
    main()
