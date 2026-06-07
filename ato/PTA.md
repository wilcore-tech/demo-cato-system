# Privacy Threshold Analysis (PTA)
## NHLBI Research Data Portal (NHLBI-RDP)

**System Identifier:** NHLBI-RDP-001
**Date Completed:** [PLACEHOLDER DATE]
**Completed By:** [PLACEHOLDER — name and title]
**Reviewed By:** [PLACEHOLDER — Privacy Officer name]

---

## Purpose

This Privacy Threshold Analysis (PTA) determines whether NHLBI-RDP collects, maintains, or disseminates Personally Identifiable Information (PII) in a manner that requires a full Privacy Impact Assessment (PIA) and/or a System of Records Notice (SORN).

---

## Threshold Questions

| # | Question | Response |
|---|---|---|
| 1 | Does the system collect, maintain, use, or disseminate information that can be used to identify an individual? | **Yes** — User account records contain name and email address. |
| 2 | Is the information retrieved by a personal identifier (name, SSN, employee ID, etc.)? | **Yes** — User accounts are retrieved by email address. |
| 3 | Does the system contain information about members of the public (non-federal employees)? | **Yes** — External researchers (non-NIH) are authorized users. |
| 4 | Does the system contain health or medical information? | **Conditionally.** Primary datasets are de-identified. No direct PHI is stored. [PLACEHOLDER — confirm with data steward.] |
| 5 | Does the system share PII with external systems or third parties? | **Yes** — Authentication events shared with NIH IdP (SAML). No researcher PII shared beyond that. |
| 6 | Is the system covered by an existing SORN? | **[PLACEHOLDER — Yes/No/Pending determination]** |

---

## Determination

Based on the responses above, a **full Privacy Impact Assessment (PIA) is required** (see `ato/PIA.md`).

A SORN determination is **[PLACEHOLDER — required/not required]**. [PLACEHOLDER — Privacy Officer to document rationale and reference applicable SORN if required.]

---

## Signatures

```
___________________________________________
[PLACEHOLDER — Completing Official Name and Title]
Date: [PLACEHOLDER]

___________________________________________
[PLACEHOLDER — Privacy Officer Name]
NIH OPDIV Privacy Officer
Date: [PLACEHOLDER]
```

---

*Document end.*
