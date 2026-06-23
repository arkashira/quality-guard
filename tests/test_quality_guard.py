import pytest
from quality_guard import QualityGuard, Webhook, Notification

def test_send_notification():
    webhooks = [Webhook("https://example.com/webhook1"), Webhook("https://example.com/webhook2", "channel1")]
    quality_guard = QualityGuard(webhooks)
    notification = Notification("main", ["metric1", "metric2"], ["2023-03-01 12:00:00", "2023-03-01 12:05:00"])
    quality_guard.send_notification(notification)

def test_create_payload():
    webhooks = [Webhook("https://example.com/webhook1"), Webhook("https://example.com/webhook2", "channel1")]
    quality_guard = QualityGuard(webhooks)
    notification = Notification("main", ["metric1", "metric2"], ["2023-03-01 12:00:00", "2023-03-01 12:05:00"])
    payload = quality_guard._create_payload(notification, webhooks[0])
    assert isinstance(payload, dict)

def test_create_slack_payload():
    webhooks = [Webhook("https://example.com/webhook1"), Webhook("https://example.com/webhook2", "channel1")]
    quality_guard = QualityGuard(webhooks)
    notification = Notification("main", ["metric1", "metric2"], ["2023-03-01 12:00:00", "2023-03-01 12:05:00"])
    payload = quality_guard._create_slack_payload(notification, webhooks[1].channel)
    assert payload["type"] == "section"
    assert payload["color"] == "danger"

def test_create_json_payload():
    webhooks = [Webhook("https://example.com/webhook1"), Webhook("https://example.com/webhook2", "channel1")]
    quality_guard = QualityGuard(webhooks)
    notification = Notification("main", ["metric1", "metric2"], ["2023-03-01 12:00:00", "2023-03-01 12:05:00"])
    payload = quality_guard._create_json_payload(notification)
    assert payload["branch"] == notification.branch
    assert payload["failed_metrics"] == notification.failed_metrics
    assert payload["timestamps"] == notification.timestamps

def test_post_to_webhook():
    webhooks = [Webhook("https://example.com/webhook1"), Webhook("https://example.com/webhook2", "channel1")]
    quality_guard = QualityGuard(webhooks)
    notification = Notification("main", ["metric1", "metric2"], ["2023-03-01 12:00:00", "2023-03-01 12:05:00"])
    payload = quality_guard._create_payload(notification, webhooks[0])
    quality_guard._post_to_webhook(webhooks[0].url, payload)

def test_post_to_webhook_failure():
    webhooks = [Webhook("https://example.com/webhook1"), Webhook("https://example.com/webhook2", "channel1")]
    quality_guard = QualityGuard(webhooks)
    notification = Notification("main", ["metric1", "metric2"], ["2023-03-01 12:00:00", "2023-03-01 12:05:00"])
    payload = quality_guard._create_payload(notification, webhooks[0])
    quality_guard.delivery_failures[webhooks[0].url] = 3
    quality_guard._post_to_webhook(webhooks[0].url, payload)
