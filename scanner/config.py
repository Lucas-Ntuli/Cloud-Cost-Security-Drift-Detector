import os


class Config:
    """Centralized configuration loaded from environment variables."""

    AZURE_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")
    TARGET_RESOURCE_GROUP = os.environ.get("TARGET_RESOURCE_GROUP")
    SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
    TF_STATE_PATH = os.environ.get("TF_STATE_PATH", "terraform.tfstate.json")
    REPORT_OUTPUT_PATH = os.environ.get("REPORT_OUTPUT_PATH", "report.md")

    @classmethod
    def validate(cls):
        """Raise an error early if required settings are missing."""
        missing = []
        if not cls.AZURE_SUBSCRIPTION_ID:
            missing.append("AZURE_SUBSCRIPTION_ID")
        if not cls.TARGET_RESOURCE_GROUP:
            missing.append("TARGET_RESOURCE_GROUP")

        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
