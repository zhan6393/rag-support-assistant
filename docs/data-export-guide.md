# Data Export Guide

How to get your data out of Acme, in bulk or on a schedule.

## Manual exports

Go to Settings > Data > Export. You can export:

- **Contacts** — CSV, up to 1,000,000 rows per export.
- **Events** — CSV or JSONL, partitioned by day.
- **Invoices** — PDF bundle.

Exports are generated asynchronously; you receive an email with a download
link when ready. Links expire after **72 hours**.

## Programmatic exports

Use `POST /v1/exports` with `{"type": "events", "format": "jsonl",
"date_from": "2025-01-01"}`. The response contains an `export_id`; poll
`GET /v1/exports/{export_id}` until `status` is `ready`, then download from
`download_url`.

Exports count against your API rate limit as a single request, regardless of
size. Very large exports (>10 GB) are split into multiple part files.

## Scheduled exports (Enterprise)

Under Settings > Data > Scheduled exports you can configure a daily or weekly
export delivered to your own S3 bucket or SFTP server. We support:

- S3 with an IAM role you create (we provide the trust policy), or
- SFTP with SSH key authentication (password auth is not supported).

## Data retention

Raw event data is retained for **13 months** on Pro and **36 months** on
Enterprise, then deleted automatically. Exports you download are yours to keep.
Deleted workspaces have their data purged after 90 days.
