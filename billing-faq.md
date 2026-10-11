# Billing FAQ

Answers to common questions about plans, invoices, and refunds.

## How am I billed?

Plans are billed **monthly in advance** on the anniversary of your signup
date. Usage-based overages (for example, extra API calls beyond your plan's
included quota) are billed **in arrears** on the next invoice.

## Where do I find my invoices?

Go to Settings > Billing > Invoices. Every invoice can be downloaded as a PDF.
Invoices are also emailed to the billing contact on file.

## How do I update my payment method?

Settings > Billing > Payment method. We accept Visa, Mastercard, Amex, and
SEPA direct debit (EU customers). Changes take effect on the next billing
cycle; they are not prorated mid-cycle.

## Can I get a refund?

- Monthly plans: refunds are available within **14 days** of the charge, as
  long as usage stayed under 10% of the plan quota.
- Annual plans: refunds are available within **30 days** of renewal.
- Overage charges are **non-refundable** once the usage has occurred.

To request a refund, contact support@acme.com with your workspace ID and the
invoice number.

## What happens if my payment fails?

We retry the charge after 24 hours, 72 hours, and 7 days. After the third
failed attempt the workspace is paused (API returns `402 Payment Required`)
until billing is resolved. No data is deleted for 90 days after pausing.
