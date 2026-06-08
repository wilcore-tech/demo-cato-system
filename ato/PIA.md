# Privacy Impact Assessment (PIA)
## NHLBI Research Data Portal (NHLBI-RDP)

**Document Version:** 1.1 — Updated to reflect Stripe payment integration (Change Ref: SIA-PR3-2026)
**Last Updated:** [PLACEHOLDER DATE]
**Next Review:** [PLACEHOLDER DATE]
**Privacy Officer:** [PLACEHOLDER]
**System Identifier:** NHLBI-RDP-001

---

## 1. System Overview

The NHLBI Research Data Portal (NHLBI-RDP) provides authenticated, role-based access to de-identified clinical research datasets maintained by the National Heart, Lung, and Blood Institute. The system is designed to make research data available to approved investigators while protecting the privacy of research subjects.

---

## 2. Personally Identifiable Information (PII) Assessment

### 2a. Does the system collect, maintain, use, or disseminate PII?

**Researcher/User PII:** Yes. The system maintains the following PII about authorized users (researchers):
- Name
- Email address (NIH or institutional)
- Institutional affiliation
- eRA Commons identifier (if applicable)
- **[NEW — v1.1]** Stripe customer ID (a pseudonymous identifier assigned by Stripe; maps to researcher account for subscription management)

This PII is used solely for account management, access control, and subscription billing. Researcher email addresses are shared with Stripe, Inc. solely for the purpose of creating a Stripe customer record. No research data, dataset contents, or clinical information is shared with Stripe. The Stripe customer relationship is governed by ISA-NHLBI-STRIPE-2026-001.

**Research Subject Data:** The primary datasets maintained in the system are **de-identified** per HIPAA Safe Harbor (45 CFR §164.514(b)) or Expert Determination standards. [PLACEHOLDER — confirm de-identification method for each dataset. If any dataset contains limited dataset identifiers under HIPAA, update this section.]

### 2b. What is the legal authority for collecting and maintaining this information?

Authority: FISMA (44 U.S.C. § 3554), NIH statutory authority under 42 U.S.C. § 281, and applicable Data Use Agreements (DUAs) with data providers. [PLACEHOLDER — cite specific SORN if applicable].

### 2c. Is a System of Records Notice (SORN) required?

[PLACEHOLDER — Privacy Officer to determine: Yes/No. If Yes, cite SORN identifier and publication date.]

---

## 3. Data Flows

| Data Element | Source | Storage | Access | Retention | Notes |
|---|---|---|---|---|---|
| User account (email, name) | NIH IdP / eRA Commons | Aurora PostgreSQL | ISSO, system admins | Duration of account + 3 years | Minimum necessary for access management |
| Audit log entries | Application | Aurora PostgreSQL + CloudWatch | ISSO, security staff | 7 years | Required by AU-11; no PII beyond user_id |
| Dataset files (de-identified) | NHLBI data stewards | Amazon S3 | Authorized researchers | Per DUA terms | De-identified; no direct PII |
| Authentication events | NIH IdP | CloudWatch (logs only) | ISSO | 7 years | SAML assertions not stored; only success/failure |
| **[NEW]** Stripe customer ID | Application (on researcher account creation) | Aurora PostgreSQL (`payment_customers` table) | Application service, ISSO | Duration of account + 3 years | Pseudonymous; email transmitted to Stripe at creation only |
| **[NEW]** Subscription records | Stripe webhook events | Aurora PostgreSQL (`subscriptions` table) | Application service, ISSO | Duration of subscription + 3 years | No research data; access tier and status only |
| **[NEW]** Stripe webhook events | Stripe, Inc. | Aurora PostgreSQL (`stripe_webhook_events` table) | Application service | 7 years (audit requirement) | Payload includes subscription event type; no PII in payload |

---

## 4. Privacy Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Re-identification of research subjects from de-identified datasets | Low | High | De-identification verified by NHLBI data stewards; data access restricted by DUA; no bulk download without DUA approval |
| Unauthorized access to researcher PII | Low | Moderate | RBAC, MFA via NIH IdP, audit logging, account lockout |
| Data breach of researcher account data | Low | Moderate | Encryption at rest and in transit; AWS KMS; immutable audit logs |
| **[NEW]** Researcher email disclosed to Stripe via API call | Low | Low | Stripe is a FedRAMP-authorized SaaS; data minimization enforced (email only, no clinical data); governed by ISA-NHLBI-STRIPE-2026-001 |
| **[NEW]** Stripe webhook replay attack enabling unauthorized subscription escalation | Low | Moderate | HMAC-SHA256 signature verification enforced on all inbound webhooks; timestamp validated within ±300 seconds to prevent replay |

---

## 5. Privacy Act Compliance

[PLACEHOLDER — Privacy Officer to complete: Determine whether the Privacy Act of 1974 applies. If a SORN covers this system, cite it here and confirm the system's use of PII is consistent with the published routine uses.]

---

## 6. Approval

```
___________________________________________
[PLACEHOLDER — Privacy Officer Name]
NIH OPDIV Privacy Officer
Date: [PLACEHOLDER]

___________________________________________
[PLACEHOLDER — ISSO Name]
Information System Security Officer
Date: [PLACEHOLDER]
```

---

*Document end.*
