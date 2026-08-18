import os
import sys
import requests

def send_slack_alert(message: str, webhook_url: str) -> None:
    """Post a message to Slack via an Incoming Webhook."""
    payload = {"text": message}

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"Failed to send Slack alert: {error}", file=sys.stderr)
        raise

def main():
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
       print("Error: SLACK_WEBHOOK_URL environment variable not set", file=sys.stderr)
       sys.exit(1)

    # Replace this with your actual drift/cost alert content
    message = "🚨 Drift detected: storage account SKU changed in eastus region."

    send_slack_alert(message, webhook_url)
    print("Slack alert sent successfully.")

if __name__ == "__main__":
    main()