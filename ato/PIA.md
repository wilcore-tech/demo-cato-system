# Privacy Impact Assessment (PIA)
## NHLBI Research Data Portal (NHLBI-RDP)

**Document Version:** 1.0
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

This PII is used solely for account management and access control. It is not shared with external parties except as required by the ISAs documented in the SSP.

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

---

## 4. Privacy Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Re-identification of research subjects from de-identified datasets | Low | High | De-identification verified by NHLBI data stewards; data access restricted by DUA; no bulk download without DUA approval |
| Unauthorized access to researcher PII | Low | Moderate | RBAC, MFA via NIH IdP, audit logging, account lockout |
| Data breach of researcher account data | Low | Moderate | Encryption at rest and in transit; AWS KMS; immutable audit logs |

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
