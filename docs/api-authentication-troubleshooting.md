# API Authentication Troubleshooting

This guide covers the most common authentication errors when calling the Acme API.

## 401 Unauthorized

A `401` response means the request did not include valid credentials.

Common causes:

- **Missing Authorization header.** Every request must include
  `Authorization: Bearer <API_KEY>`.
- **Revoked or rotated key.** Keys can be revoked from the dashboard under
  Settings > API Keys. If a key was rotated, old keys stop working immediately.
- **Wrong environment.** Sandbox keys start with `sk_test_` and only work
  against `api.sandbox.acme.com`. Production keys start with `sk_live_` and
  only work against `api.acme.com`.

To fix: regenerate a key in the dashboard, then retry with
`curl -H "Authorization: Bearer sk_live_..." https://api.acme.com/v1/ping`.

## 403 Forbidden

A `403` means the key is valid but lacks permission for the resource.

Common causes:

- The key's role is **read-only** but the endpoint requires write access.
- The request targets a different workspace than the key belongs to.

To fix: check the key's role under Settings > API Keys, or create a new key
with the `admin` role.

## Token expiry

OAuth access tokens expire after **60 minutes**. When you receive
`{"error": "token_expired"}`, use your refresh token to obtain a new access
token via `POST /oauth/token` with `grant_type=refresh_token`.
