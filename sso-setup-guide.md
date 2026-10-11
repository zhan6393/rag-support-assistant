# SSO / SAML Setup Guide

This guide walks through configuring Single Sign-On for your workspace.
SSO is available on Pro and Enterprise plans.

## Prerequisites

- You must be a workspace **admin**.
- Your identity provider (Okta, Entra ID, Google Workspace, or any
  SAML 2.0 IdP) must support signed AuthnRequests.

## Step 1 — Add Acme as an application in your IdP

- **ACS (Assertion Consumer Service) URL:**
  `https://app.acme.com/sso/acs`
- **Entity ID:** `urn:acme:sso:<WORKSPACE_ID>`
- **NameID format:** Email address
- Map the `email`, `firstName`, and `lastName` attributes.

## Step 2 — Enter IdP details in Acme

Go to Settings > Security > Single Sign-On and paste:

1. The IdP metadata XML (or metadata URL), and
2. The X.509 signing certificate.

## Step 3 — Test before enforcing

Use **Test login** to verify with your own account. Only after a successful
test should you toggle **Require SSO for all members**. If SSO is misconfigured
and enforced, admins can still sign in with a recovery code from
Settings > Security (keep these codes in a safe place).

## SCIM provisioning (Enterprise)

Enable SCIM with the base URL `https://api.acme.com/scim/v2` and a bearer
token generated under Settings > Security > SCIM. Deprovisioned users lose
access immediately; their data is retained for 30 days.

## Common errors

- `SAML audience mismatch` — the Entity ID in your IdP does not match
  `urn:acme:sso:<WORKSPACE_ID>`.
- `Clock skew` — if the IdP and Acme disagree by more than 3 minutes on the
  assertion timestamp, login fails. Enable NTP on the IdP host.
