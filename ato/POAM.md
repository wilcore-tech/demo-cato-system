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
| Medium | **2** | 0 | 0 |
| Low | [PLACEHOLDER] | [PLACEHOLDER] | 0 |
| **Total Open** | **2+** | | |

The system maintains zero critical and zero high findings. Two medium findings are actively tracked below. The system is in good standing with its Authorization to Operate.

---

## Open Findings

A Security Impact Analysis (SIA) has been initiated for wilcore-tech/demo-cato-system#PR3 affecting the NIH Grant Portal (Transformative tier). The SIA will assess security implications of the proposed changes and determine if additional POA&M items are warranted prior to deployment authorization.

Supply Chain Risk Management Plan updated per SIA requirements for NIH Grant Portal (wilcore-tech/demo-cato-system#PR3, Tier: Transformative). New dependency inventory and vendor assessment controls documented in SCRM baseline. Mitigation tracking assigned to Infrastructure team with quarterly validation gates.

Authorization Boundary Diagram update required to reflect architectural changes introduced in wilcore-tech/demo-cato-system#PR3. This diagram revision is classified as Transformative tier and impacts the NIH Grant Portal system authorization scope. Update must be completed and reviewed by AO before closure of this finding.

ISA documentation for the NIH Grant Portal external system connection (referenced in wilcore-tech/demo-cato-system#PR3, Tier: Transformative) is required and must be completed prior to system authorization. The ISA shall address data flows, authentication mechanisms, and boundary protection controls between NHLBI-RDP and the Grant Portal.

SSP control descriptions for AC-2, AC-3, AC-4, AC-6, AU-12, and AU-2 require updates to reflect changes implemented in wilcore-tech/demo-cato-system#PR3 (Transformative tier). These updates align access control and audit logging mechanisms with current NIH Grant Portal operational requirements and are scheduled for completion in the current review cycle.

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

A Significant Change Notification (SCN) has been generated and submitted to the Authorizing Official for wilcore-tech/demo-cato-system#PR3, classified as a Transformative-tier change affecting the NIH Grant Portal system architecture. The SCN documents the proposed modifications and requests formal approval prior to implementation. AO response is pending and will be recorded upon receipt.

The Authorizing Official has reviewed the current POA&M and accepts the residual risk represented by the open findings, contingent on remediation by the scheduled dates.

```
___________________________________________
[PLACEHOLDER — AO Name]
Authorizing Official
Date: [PLACEHOLDER]
```