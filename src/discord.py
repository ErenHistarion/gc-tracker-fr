import requests
import json

from src.logger import get_logger

logger = get_logger(__name__)


def send_discord_notification(
    message,
    webhook_url="https://discord.com/api/webhooks/***",
):
    data = {"content": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)

    if response.status_code == 204:
        nothing_to_do = True
        # logger.debug("Notification send to Discord")
    else:
        logger.error(f"Discord error: {response.status_code}")
