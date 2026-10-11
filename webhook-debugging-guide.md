# Webhook Debugging Guide

If your endpoint is not receiving webhooks, work through this checklist.

## 1. Is the webhook enabled?

Go to Settings > Webhooks and confirm the endpoint shows **Active** (not
Paused). New endpoints start paused until the first successful delivery.

## 2. Did the handshake succeed?

When you register an endpoint, we send a `webhook.handshake` event containing
a `challenge` token. Your endpoint must respond within 5 seconds with HTTP 200
and echo the challenge in the response body. Until the handshake succeeds, no
real events are delivered.

## 3. Check the delivery log

Every delivery attempt is logged under Settings > Webhooks > Delivery log,
with the HTTP status your endpoint returned. Common failure codes:

- `410 Gone` — we auto-disable endpoints after 50 consecutive 410s.
- `429` from your server — we back off for 1 hour, then retry.
- Timeouts (>10s) — 5 retries with exponential backoff, then the event is
  moved to the dead-letter queue (retained 7 days).

## 4. Verify the signature

Each request carries an `X-Acme-Signature` header: HMAC-SHA256 of the raw
request body, keyed with your webhook secret. If your code parses the JSON
before verifying, whitespace differences will break the signature — always
verify against the **raw body bytes**.

## 5. Event filtering

If you subscribed to specific event types only, events outside the filter are
never sent. Check the endpoint's event filter list; `*` subscribes to all.
