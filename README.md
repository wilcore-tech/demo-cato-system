# demo-cato-system

This repository is a **synthetic federal web application** purpose-built for demonstrating the [cATO Advisor](https://github.com/wilcore-tech/cato-advisor) tool. It simulates a real federal system — the NHLBI Research Data Portal — that holds an active Authorization to Operate (ATO) in good standing.

The repo exists so demo reviewers can open pull requests against it and watch the cATO Advisor detect what tier of ATO artifact impact each change represents, without touching any real system.

---

## Repository Structure

```
demo-cato-system/
├── app/                          # Fake federal web application (Python/FastAPI)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src/
│   │   ├── main.py               # FastAPI entry point
│   │   ├── auth/
│   │   │   └── config.py         # SAML/session/auth config
│   │   ├── api/
│   │   │   └── client.py         # External HTTP client (NCBI API)
│   │   └── db/
│   │       └── migrations/
│   │           └── 001_init.sql  # Initial database schema
│   ├── k8s/
│   │   ├── deployment.yaml
│   │   └── ingress.yaml          # Port 443 ingress
│   └── terraform/
│       ├── main.tf               # ECS cluster + service
│       ├── network.tf            # VPC, subnets, security groups, ALB
│       └── iam.tf                # IAM roles (least privilege)
├── .github/
│   └── workflows/
│       └── ci.yml                # CI pipeline (lint, test, docker build, Trivy scan)
├── ato/                          # ATO artifact documents
│   ├── SSP.md                    # System Security Plan (NIST SP 800-18 structure)
│   ├── POAM.md                   # Plan of Action & Milestones
│   ├── IRP.md                    # Incident Response Plan
│   ├── CP.md                     # Contingency Plan
│   ├── CMP.md                    # Configuration Management Plan
│   ├── PIA.md                    # Privacy Impact Assessment
│   ├── PTA.md                    # Privacy Threshold Analysis
│   └── ATO_LETTER.md             # Authorization decision letter (good standing baseline)
└── README.md
```

---

## Demo Branches and FedRAMP Change Tiers

The repo includes three pre-scripted branches, each designed to trigger a specific classification tier in the cATO Advisor diff analyzer. There is a fourth tier — **Emergency** — that these branches do not cover (it is for unplanned incident-driven changes).

| Branch | Tier | What Changes | Why This Tier |
|---|---|---|---|
| `demo/routine` | **Routine Recurring** | `requests` bumped 2.28.0 → 2.31.0; CI action updated to `checkout@v4` | Dependency patch within existing boundary; no security control change |
| `demo/adaptive` | **Adaptive** | `auth/config.py` adds `MFA_REQUIRED = True`; new `nginx/nginx.conf` enforces TLS 1.3 | Modifies existing security controls (IA-2, SC-8) but stays within authorized boundary |
| `demo/transformative` | **Transformative** | New `payments/stripe_client.py` (external data flow); new DB migration; new port 8443 in ingress; new `terraform/secrets.tf` | New external integration, new port exposure, new data flow — requires AO re-authorization |

### Tier Definitions (from CMP.md)

- **Routine Recurring** — Low-risk, pre-authorized changes within established parameters. No AO re-authorization required.
- **Adaptive** — Changes to existing security controls that remain within the authorized boundary. AO notification required; no re-authorization.
- **Transformative** — Changes that materially alter the system boundary, introduce new external data flows, or expose new ports/services. Full Security Impact Analysis and AO re-authorization required.
- **Emergency** — Unplanned changes for active incident response. Retroactive documentation required.

---

## Instructions for Matt — Filling in Placeholders

Every `[PLACEHOLDER]` field in the `ato/` documents needs to be filled in before the demo (or left as-is if you want to show the tool detecting that ATO docs are stale/incomplete).

### Static fields — fill once

These are identity/personnel fields that don't change:

| Document | Field | What to Put |
|---|---|---|
| All `ato/` files | `[PLACEHOLDER — AO Name]` | Pick a fictional AO name, e.g., "Dr. Sandra L. Reyes" |
| All `ato/` files | `[PLACEHOLDER — ISSO Name]` | Pick a fictional ISSO name, e.g., "Marcus J. Webb" |
| `ato/SSP.md` | Key Personnel table | Fill all roles with fictional names/contacts |
| `ato/SSP.md` | External Integrations — agreement numbers | Fictional ISA/MOU numbers, e.g., "ISA-NIH-OCIO-2024-001" |
| `ato/ATO_LETTER.md` | Authorization Date / Expiration | Already set: June 7, 2025 / June 7, 2029 |
| `ato/POAM.md` | Quarterly Review Log | Add a couple of fictional quarterly entries |

### Date fields — fill before each demo run

| Document | Field | Suggested Value |
|---|---|---|
| `ato/SSP.md` | `[CURRENT — last updated: PLACEHOLDER DATE]` (in each control section) | Set to a date ~6 months ago to show "recently reviewed" |
| `ato/POAM.md` | Date Identified for both findings | 3–6 months ago |
| `ato/POAM.md` | Target remediation dates | A few weeks in the future |
| `ato/IRP.md` / `CP.md` | Last exercise/test dates | 6 months ago |

### Fields that would be auto-updated by a real cATO pipeline

In a live cATO implementation, these would be stamped automatically when a change is authorized:

- `[CURRENT — last updated: PLACEHOLDER DATE]` markers in each SSP control section
- POAM status and finding dates
- ATO Letter authorization date (on re-authorization events)

---

## Relationship to cATO Advisor

The [cATO Advisor](https://github.com/wilcore-tech/cato-advisor) tool analyzes pull requests opened against this repo and:

1. Diffs the changed files against the main branch
2. Classifies the change tier (Routine / Adaptive / Transformative / Emergency)
3. Identifies which ATO artifact sections are impacted by the change
4. Recommends which `ato/` documents need to be updated before the change can be authorized

To run the demo: open a PR from one of the three `demo/*` branches into `main` and trigger the cATO Advisor analysis.
