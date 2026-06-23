# Quality Guard

A Python project for sending notifications on CI run failures.

## Usage

1. Create a `QualityGuard` instance with a list of `Webhook` objects.
2. Create a `Notification` object with the branch, failed metrics, and timestamps.
3. Call the `send_notification` method on the `QualityGuard` instance.

## Testing

Run the tests using `pytest`.
