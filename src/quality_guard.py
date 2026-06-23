import json
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import time
from typing import List

@dataclass
class Webhook:
    url: str
    channel: str = None

@dataclass
class Notification:
    branch: str
    failed_metrics: List[str]
    timestamps: List[str]

class QualityGuard:
    def __init__(self, webhooks: List[Webhook]):
        self.webhooks = webhooks
        self.delivery_failures = {}

    def send_notification(self, notification: Notification):
        for webhook in self.webhooks:
            payload = self._create_payload(notification, webhook)
            self._post_to_webhook(webhook.url, payload)

    def _create_payload(self, notification: Notification, webhook: Webhook):
        if webhook.channel:
            return self._create_slack_payload(notification, webhook.channel)
        else:
            return self._create_json_payload(notification)

    def _create_slack_payload(self, notification: Notification, channel: str):
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"CI run failed on {notification.branch} at {notification.timestamps[0]}"
            },
            "color": "danger",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Failed metrics: {', '.join(notification.failed_metrics)}"
                    }
                }
            ]
        }

    def _create_json_payload(self, notification: Notification):
        return {
            "branch": notification.branch,
            "failed_metrics": notification.failed_metrics,
            "timestamps": notification.timestamps
        }

    def _post_to_webhook(self, url: str, payload: dict):
        if url in self.delivery_failures:
            if self.delivery_failures[url] >= 3:
                logging.error(f"Failed to deliver notification to {url} after 3 retries")
                return
            time.sleep(2 ** self.delivery_failures[url])
        try:
            # Simulate a POST request
            logging.info(f"Posting to {url}: {json.dumps(payload)}")
        except Exception as e:
            logging.error(f"Failed to deliver notification to {url}: {e}")
            self.delivery_failures[url] = self.delivery_failures.get(url, 0) + 1
            self._post_to_webhook(url, payload)

def main():
    webhooks = [Webhook("https://example.com/webhook1"), Webhook("https://example.com/webhook2", "channel1")]
    quality_guard = QualityGuard(webhooks)
    notification = Notification("main", ["metric1", "metric2"], ["2023-03-01 12:00:00", "2023-03-01 12:05:00"])
    quality_guard.send_notification(notification)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
