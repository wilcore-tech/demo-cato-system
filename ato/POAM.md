# Plan of Action & Milestones (POA&M)
## NHLBI Research Data Portal (NHLBI-RDP)

**System Identifier:** NHLBI-RDP-001
**FISMA Impact Level:** Moderate
**Reporting Period:** [PLACEHOLDER — current quarter, e.g., Q3 FY2025]
**Last Updated:** [PLACEHOLDER DATE]
**ISSO:** [PLACEHOLDER]

---

## Executive Summary

| Risk Level | Open | Closed This Quarter | Overdue |
|---|---|---|---|
| Critical | **0** | 0 | 0 |
| High | **0** | 0 | 0 |
| Medium | **3** | 0 | 0 |
| Low | [PLACEHOLDER] | [PLACEHOLDER] | 0 |
| **Total Open** | **3+** | | |

The system maintains zero critical and zero high findings. Three medium findings are actively tracked below, including one newly identified during SAML authentication implementation (Change 4992E39C). The system is in good standing with its Authorization to Operate.
## Open Findings

### POA&M-2025-001 — Dependency Vulnerability: requests library (CVE-2023-32681)

| Field | Value |
|---|---|
| Finding ID | POA&M-2025-001 |
| Severity | Medium |
| Source | Automated dependency scan (Trivy) |
| Date Identified | [PLACEHOLDER — scan date] |
| Control(s) Affected | SI-2 (Flaw Remediation), SR-3 (Supply Chain Controls) |
| Vulnerability | The `requests` library version 2.28.0 has a known SSRF (Server-Side Request Forgery) vulnerability in how it handles certain redirect scenarios (CVE-2023-32681). CVSS 3.1 Base Score: 6.1 (Medium). |
| Affected Component | `app/requirements.txt` — `requests==2.28.0` |
| Remediation Plan | Upgrade `requests` to version 2.31.0 or later, which contains the fix. Update will require regression testing of external API integrations. |
| Target Completion | [PLACEHOLDER — within 60 days of ATO refresh] |
| Responsible Party | [PLACEHOLDER — Development Lead] |

---

### POA&M-2025-002 — SAML Assertion Encryption Configuration

| Field | Value |
|---|---|
| Finding ID | POA&M-2025-002 |
| Severity | Medium |
| Source | Security Impact Analysis (Change 4992E39C) |
| Date Identified | [PLACEHOLDER — SIA completion date] |
| Control(s) Affected | IA-5 (Authenticator Management), SC-12 (Cryptographic Key Establishment) |
| Issue | SAML assertion encryption parameters and token expiration policies require formal documentation and configuration validation against FedRAMP baselines. |
| Affected Component | `config/auth.yaml` — SAML IdP integration |
| Remediation Plan | Document SAML token expiration (TTL), replay protection mechanisms, and assertion encryption cipher suites in updated SSP Section 2.13. Validate IdP certificate chain and establish key rotation schedule per SC-12. |
| Target Completion | [PLACEHOLDER — within 30 days of this POA&M update] |
| Responsible Party | [PLACEHOLDER — ISSO / Security Engineering] |
### POA&M-2025-001 — Dependency Vulnerability: requests library (CVE-2023-32681)

| Field | Value |
|---|---|
| Finding ID | POA&M-2025-001 |
| Severity | Medium |
| Source | Automated dependency scan (Trivy) |
| Date Identified | [PLACEHOLDER — scan date] |
| Control(s) Affected | SI-2 (Flaw Remediation), SR-3 (Supply Chain Controls) |
| Vulnerability | The `requests` library version 2.28.0 has a known SSRF (Server-Side Request Forgery) vulnerability in how it handles certain redirect scenarios (CVE-2023-32681). CVSS 3.1 Base Score: 6.1 (Medium). |
| Affected Component | `app/requirements.txt` — `requests==2.28.0` |
| Remediation Plan | Upgrade `requests` to version 2.31.0 or later, which contains the fix. Update will require regression testing of external API client (`app/src/api/client.py`) before deployment to production. |
| Responsible Party | [PLACEHOLDER — developer name or team] |
| Original Target Date | [PLACEHOLDER] |
| Revised Target Date | [PLACEHOLDER] |
| Milestone 1 | Complete regression test suite update — [PLACEHOLDER DATE] |
| Milestone 2 | Deploy to staging and validate — [PLACEHOLDER DATE] |
| Milestone 3 | Deploy to production — [PLACEHOLDER DATE] |
| Status | **In Progress** |
| AO Accepted Risk | No — active remediation required |

---

### POA&M-2025-002 — CI/CD Action Version — Unpinned SHA (GitHub Actions)

| Field | Value |
|---|---|
| Finding ID | POA&M-2025-002 |
| Severity | Medium |
| Source | Manual code review / supply chain risk assessment |
| Date Identified | [PLACEHOLDER — review date] |
| Control(s) Affected | SA-10 (Developer Configuration Management), SR-3 (Supply Chain Controls), CM-2 (Baseline Configuration) |
| Vulnerability | The CI workflow (`.github/workflows/ci.yml`) uses `actions/checkout@v3`, which is not pinned to a specific commit SHA. This creates a supply chain risk: a compromised or hijacked tag could execute malicious code in the CI pipeline without a version change being visible in the diff. CVSS equivalent: Medium (supply chain integrity). |
| Affected Component | `.github/workflows/ci.yml` — `uses: actions/checkout@v3` |
| Remediation Plan | (1) Upgrade to `actions/checkout@v4` (latest stable), (2) Pin to the full commit SHA of that release (e.g., `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683`), (3) Add Dependabot configuration to auto-update pinned SHA digests for GitHub Actions. |
| Responsible Party | [PLACEHOLDER — DevOps/Platform team] |
| Original Target Date | [PLACEHOLDER] |
| Revised Target Date | [PLACEHOLDER] |
| Milestone 1 | Update action versions and pin SHAs in CI workflow — [PLACEHOLDER DATE] |
| Milestone 2 | Configure Dependabot for Actions updates — [PLACEHOLDER DATE] |
| Status | **In Progress** |
| AO Accepted Risk | No — active remediation required |

---

## Closed Findings (Current Period)

*No findings closed this quarter. [PLACEHOLDER — update as findings are remediated.]*

---

## Quarterly Review Log

| Quarter | Reviewer | Date | Finding Count (Open) | Notes |
|---|---|---|---|---|
| Q1 FY2025 | [PLACEHOLDER] | [PLACEHOLDER] | 2 Medium | Initial findings from security assessment |
| Q2 FY2025 | [PLACEHOLDER] | [PLACEHOLDER] | 2 Medium | Remediation milestones on track |
| Q3 FY2025 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Q4 FY2025 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## AO Acknowledgment

The Authorizing Official has reviewed the current POA&M and accepts the residual risk represented by the open findings, contingent on remediation by the scheduled dates.

```
___________________________________________
[PLACEHOLDER — AO Name]
Authorizing Official
Date: [PLACEHOLDER]
```