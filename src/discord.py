import requests
import json

from src.logger import get_logger

logger = get_logger(__name__)


def send_discord_notification(
    message,
    webhook_url="https://discord.com/api/webhooks/1358016683117121658/pw1fIdFl54janX-e5-h-usNfJdU893z7YTYQGOLPs5oXaxxyLOjjqcrooE1-t2t45eM5",
):
    data = {"content": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)

    if response.status_code == 204:
        nothing_to_do = True
        # logger.debug("Notification send to Discord")
    else:
        logger.error(f"Discord error: {response.status_code}")
