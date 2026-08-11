# Cloud Cost and Security Drift Detector

Automatically detects when live Azure infrastructure has diverged from its Terraform definition, flags security misconfigurations against AZ-500-aligned controls and estimates the cost impact on a daily schedule via GitHub Actions.

# Why this project exists

Infrastructure-as-code only guarantees correctness at the moment of terraform apply command. After that, anyone with the portal access can change a setting manually resulting widening a firewall rule, make a storage container public, disable purge protection and noting catches it until an incident happens. This tool closes that gap.

# Architecture

```

terraform/
scanner/
  config.py
  tf_state.py
  azure_client.py
  drift.py
  policies.py
  cost.py
  report.py
  main.py
.github/workflows/
```

# Design decisions worth explaining in an interview

Drift vs policy are separate engines. Drift means Terraform and Azure disagree. Policy means this configuration is unsafe, regardless of whether it matches the code. A baseline can be policy-complaint but still drift or drift-free but still insecure, they are orthogonal and conflating them would hide real issues.

OpenID connect login instead of stored credentials in the GitHub Actions workflow, no longer-lived secret sits in the repo, Azure trusts GitHub token exchange directly.

Non-root docker user for the scanner itself, the tool that audits security should follow the same practises it enforces.

Exit code gates the pipelines. critical findings fail the build, so this sit in front of a deployment pipeline, not just run as a side report nobody reads.

# Setup

1. cd terraform && terraform init $$ terraform apply to create the watched baseline infrastructure.

2. Create a Service Principal with Reader + Security Reader on the subscription and configure OpenID Connect federation for GitHub Actions.

3. Set repo secrets: AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_SUSCRIPTION_ID, optionally SLACK_WEBHOOK_URL.

4. Set repo variable TARGET_RESOURCE_GROUP to the G name from step 1.

5. Push to main or trigger the workflow manually as it also runs daily.

# Local run

```
cd scanner
pip install -r requirements.txt
az login
export AZURE_SUBSCRIPTION_ID=<sub-id>
export TARGET_RESOURCE_GROUP=<rg-name>
export TF_STATE_PATH=../terraform/terraform.tfstate
python main.py
```

# Roadmap

things to build next, to keep this project growing:
1. Extend policy checks to Azure SQL/App Service configurations.

2. Replace flat cost estimate with real Cost management API usage data.

3. Add a small web dashboard.

4. Auto-remediate low-risk findings via a terraform apply gated by manual approval.
