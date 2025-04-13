import requests
import json
import yaml

from src.logger import get_logger

logger = get_logger(__name__)

with open("./src/config/config.yml", "r") as file:
    configs = yaml.safe_load(file)["discord"]

WEBHOOK_URL = configs["WEBHOOK_URL"]


def send_discord_notification(
    message,
    webhook_url=WEBHOOK_URL,
):
    data = {
        "content": message,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)

    if response.status_code == 204:
        nothing_to_do = True
        # logger.debug("Notification send to Discord")
    else:
        logger.error(f"Discord error: {response.status_code}")
