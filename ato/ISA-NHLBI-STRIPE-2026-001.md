# Interconnection Security Agreement
## ISA-NHLBI-STRIPE-2026-001
### NHLBI Research Data Portal ↔ Stripe Payments API

**Agreement Version:** 1.0 — DRAFT (Pending Legal and AO Review)
**Effective Date:** [PLACEHOLDER — execute before production deployment]
**Review Date:** [PLACEHOLDER — annually from effective date]
**Classification:** FOR OFFICIAL USE ONLY (FOUO)

---

## 1. Parties

| Role | Organization | Contact |
|---|---|---|
| Government System Owner | National Heart, Lung, and Blood Institute (NHLBI) | [PLACEHOLDER — Mission Owner] |
| ISSO | NHLBI | [PLACEHOLDER — ISSO name and email] |
| External System Owner | Stripe, Inc. | agreements@stripe.com |
| Authorizing Official | NIH OCIO | [PLACEHOLDER — AO name] |

---

## 2. Purpose

This agreement documents the security terms governing the interconnection between the NHLBI Research Data Portal (NHLBI-RDP, FISMA ID: NHLBI-RDP-001, FISMA Moderate) and the Stripe Payments API (a FedRAMP-authorized SaaS) for the purpose of subscription-based data access billing.

The interconnection was authorized as part of Change CHG-2026-PR3 (classified: Transformative) and requires AO acknowledgment per FedRAMP Transformative change requirements.

---

## 3. Interconnection Description

| Attribute | Value |
|---|---|
| Connection type | Outbound HTTPS (TLS 1.2+) from NHLBI-RDP application tier |
| Destination | api.stripe.com:443 |
| Inbound (webhooks) | /payments/webhook endpoint on NHLBI-RDP, port 443 |
| Authentication (outbound) | Bearer token (Stripe secret key) from AWS Secrets Manager |
| Authentication (inbound webhooks) | HMAC-SHA256 signature verification (Stripe-Signature header) |
| Data transmitted outbound | Researcher email (account creation only), subscription management commands |
| Data received inbound | Subscription lifecycle events (created, updated, canceled, payment_failed) |
| Research data transmitted | **None** — no clinical data, datasets, or subject identifiers are transmitted |
| PII transmitted | Researcher email address only |

---

## 4. Security Controls

| Control | Implementation |
|---|---|
| SC-8 (Transmission Confidentiality) | TLS 1.2+ enforced; `verify=True` on all outbound calls |
| SC-12 (Key Management) | Stripe credentials stored in AWS Secrets Manager; rotated every 90 days |
| AC-4 (Information Flow) | Egress restricted to api.stripe.com:443 via security group; no research data in payload |
| AU-2 (Event Logging) | All Stripe API calls logged; all webhook events stored in `stripe_webhook_events` table |
| SI-10 (Information Input Validation) | Webhook payloads HMAC-verified before processing; timestamp validated ±300s |
| CA-3 (Information Exchange) | Documented in this ISA; reviewed annually |

---

## 5. Data Minimization Confirmation

The ISSO confirms that:
- No de-identified or identifiable research subject data is transmitted to Stripe
- No clinical records, dataset contents, or HIPAA-covered information is in scope
- PII transmitted is limited to researcher email address for Stripe customer creation

---

## 6. Stripe FedRAMP Status

Stripe, Inc. operates under a FedRAMP authorization. [PLACEHOLDER — ISSO to verify current FedRAMP authorization status at marketplace.fedramp.gov prior to execution and annually thereafter.]

---

## 7. Approval and Signatures

| Role | Name | Signature | Date |
|---|---|---|---|
| ISSO (NHLBI-RDP) | [PLACEHOLDER] | _________________ | [PLACEHOLDER] |
| Mission Owner | [PLACEHOLDER] | _________________ | [PLACEHOLDER] |
| Authorizing Official | [PLACEHOLDER] | _________________ | [PLACEHOLDER] |
| Stripe Representative | [PLACEHOLDER] | _________________ | [PLACEHOLDER] |

---

*This ISA must be executed and signed before the Stripe payment integration is deployed to production.*
