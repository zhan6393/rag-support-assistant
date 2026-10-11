# Rate Limiting Guide

The Acme API enforces rate limits to keep the platform stable for everyone.

## Limits

| Plan        | Requests / minute | Burst |
|-------------|-------------------|-------|
| Free        | 60                | 10    |
| Pro         | 600               | 50    |
| Enterprise  | 5,000             | 200   |

## 429 Too Many Requests

When you exceed your limit, the API returns `429` with a JSON body:

```json
{ "error": "rate_limit_exceeded", "retry_after_ms": 4500 }
```

The response also includes a `Retry-After` header (in seconds).

## Best practices

1. **Back off exponentially.** On a `429`, wait `retry_after_ms`, then double
   the wait on each subsequent `429`, up to a maximum of 60 seconds.
2. **Add jitter.** Randomize waits by ±20% so many clients do not retry in
   lockstep (the thundering-herd problem).
3. **Cache aggressively.** Most `GET` responses include an `ETag`; send
   `If-None-Match` to get a cheap `304 Not Modified` instead of full data.
4. **Batch writes.** The `/v1/batch` endpoint accepts up to 100 operations per
   call and counts as a single request against your limit.

## Monitoring usage

Current usage is visible in the dashboard under Usage > API, and
programmatically via `GET /v1/rate_limit_status`, which returns your remaining
quota and reset timestamp.
