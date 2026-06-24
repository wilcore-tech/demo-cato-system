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

**Significant Change Notification (SCN) — Transformative Tier**

On 2025-01-15, the NHLBI Research Portal integrated Stripe payment processing API with associated PostgreSQL schema expansion for financial transaction data, network ingress reconfiguration for third-party API endpoints, and AWS Secrets Manager hardening for API key rotation. This change expands the system boundary to include cardholder data environment (CDE) scope and introduces external service dependency risk. AO acknowledgment and supplemental security assessment required before production deployment. Change ticket: wilcore-tech/demo-cato-system#PR3.

POAM-2025-003 | HIGH | AC-2, AC-3, AC-4, AC-6 | Stripe payment API integration introduces new external service dependency and financial transaction data scope requiring expanded access controls and account provisioning procedures. Stripe API credentials stored in HashiCorp Vault with automated rotation policy (90-day cycle); database schema expanded to include PCI-relevant fields (card tokens, transaction metadata) requiring enhanced AC-6 privileged access restrictions and role-based access controls for finance and operations staff. Discovered: 2025-01-08. Owner: Security Engineering Team. Target: 2025-02-15. Status: IN PROGRESS — AC-2/AC-3 role definitions completed (evidence: access-control-matrix-v2.1, vault-audit-log-2025-01-12), AC-4 network ingress policies (payment subnet isolation) deployed to staging, production deployment and AU-12 audit logging expansion scheduled 2025-02-10.

POAM-2025-003 | HIGH | SA-9, SC-7 | External payment processing API integration (Stripe) introduces new third-party dependency and financial data handling scope. Discovered: 2025-01-15. Owner: Security Engineering Team. Target: 2025-02-28. Status: IN PROGRESS — Interconnection Security Agreement (ISA) with Stripe drafted and under legal review; network ingress rules for API gateway restricted to Stripe IP ranges (172.56.0.0/13) implemented in staging (evidence: change-ticket-5847, network-policy-2025-01-14). Database schema encryption for payment card data (at-rest AES-256, in-transit TLS 1.2+) configured and validated in non-production environment. Production deployment and ISA signature target 2025-02-28.

POA&M-2025-003 | HIGH | CA-9, SC-7 | Authorization Boundary Diagram requires update to reflect Stripe payment API integration, expanded database schema for financial transaction data, and network ingress reconfiguration. Discovered: 2025-01-15. Owner: Architecture Review Board. Target: 2025-02-28. Status: IN PROGRESS — System boundary documentation updated to include third-party API dependencies and secrets management hardening for API keys (evidence: PR3-architectural-review-2025-01-15); network diagram revision and NIST mapping validation scheduled for completion by 2025-02-21.

POA&M-2025-003 | HIGH | SA-9, SC-7 | Third-party payment processing API (Stripe) integration introduces external dependency and expanded system boundary. New financial transaction data classification requires secrets management hardening for API keys and webhook credentials, network ingress rule expansion for Stripe service endpoints, and database schema changes to support payment records. Discovered: 2025-01-15. Owner: Security Engineering & Platform Team. Target: 2025-02-28. Status: IN PROGRESS — Stripe API key rotation mechanism implemented in secrets vault (evidence: PR3-secrets-config-commit), network ACL changes staged for review (evidence: change-ticket-5143), payment data handling controls assessment scheduled 2025-01-22.

POA&M-2025-003 | HIGH | SA-3, SC-7, IA-4 | External Payment API Integration — Stripe dependency introduces new network ingress pathway, secrets management scope expansion, and third-party risk surface. Database schema extended to store payment card metadata requiring PCI DSS alignment controls. Discovered: 2025-01-15. Owner: Security Engineering Team. Target: 2025-02-28. Status: IN PROGRESS — API credential rotation policy implemented 2025-01-18; network segmentation rule set deployed to staging 2025-01-22; PCI scoping assessment scheduled 2025-02-05 (evidence: PR3-security-checklist, network-config-PR-847, vendor-risk-matrix-v2.1).

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
