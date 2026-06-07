# Configuration Management Plan (CMP)
## NHLBI Research Data Portal (NHLBI-RDP)

**Document Version:** 1.0
**Classification:** FOR OFFICIAL USE ONLY (FOUO)
**Last Updated:** [PLACEHOLDER DATE]
**Next Review:** [PLACEHOLDER DATE]
**ISSO:** [PLACEHOLDER]

---

## 1. Purpose and Scope

This Configuration Management Plan (CMP) defines the processes and controls for managing the configuration of NHLBI-RDP throughout its operational life. It implements NIST SP 800-128 (Guide for Security-Focused Configuration Management of Information Systems) and satisfies CM family controls under NIST SP 800-53 Rev 5.

---

## 2. Configuration Items

The following items constitute the configuration baseline for NHLBI-RDP:

| CI Type | Location | Owner | Change Process |
|---|---|---|---|
| Application source code | GitHub (`wilcore-tech/demo-cato-system`) | Development Lead | Pull Request + review |
| Container image | Amazon ECR | DevOps | CI/CD pipeline |
| Infrastructure (Terraform) | GitHub (`app/terraform/`) | DevOps | Pull Request + review + plan review |
| Kubernetes manifests | GitHub (`app/k8s/`) | DevOps | Pull Request + review |
| Authentication configuration | `app/src/auth/config.py` | ISSO + Dev Lead | Pull Request + ISSO review |
| Secrets | AWS Secrets Manager | ISSO | Change ticket + ISSO approval |
| Database schema | `app/src/db/migrations/` | DBA | Pull Request + DBA + ISSO review |

---

## 3. Change Classification Framework

All changes are classified before implementation. Classification determines the required review, approval, and documentation process.

| Tier | Definition | Examples | Required Approvals | AO Re-Authorization? |
|---|---|---|---|---|
| **Routine Recurring** | Low-risk, pre-authorized changes within established parameters. Follows a documented standard operating procedure. | Patch/dependency version bump (no CVE fix), CI tooling update, documentation update | ISSO review (post-implementation) | No |
| **Adaptive** | Changes to existing security controls or configurations that remain within the authorized boundary. Risk is understood and bounded. | New MFA requirement, TLS version change, IAM policy tightening, authentication flow update | ISSO review + AO notification | No (notify AO) |
| **Transformative** | Changes that materially alter the system boundary, introduce new external data flows, expose new ports/services, or add significant new functionality. | New external API integration, new database table with PII, new port exposure, new cloud service | ISSO + ISO + AO review | **Yes — full SIA required** |
| **Emergency** | Unplanned changes required to address an active security incident or critical system failure. Requires retroactive documentation. | Emergency patch for active exploit, emergency firewall rule, emergency secret rotation | Incident Commander + AO notification within 1 hour | Post-implementation SIA |

---

## 4. Change Management Process

### Standard Change Process (Routine Recurring / Adaptive)

1. Developer opens a Pull Request in GitHub with a description of the change.
2. CI pipeline runs automated checks (lint, test, security scan).
3. Pull Request is reviewed by at least one peer reviewer.
4. ISSO reviews changes affecting security-relevant files (authentication, authorization, network configuration, secrets, infrastructure).
5. Change is merged to `main` by authorized merger.
6. Deployment to staging is automated via CI/CD.
7. Production deployment requires manual approval in the CI/CD pipeline by [PLACEHOLDER — authorized approvers].
8. ISSO records change in the change log [PLACEHOLDER — change log location] post-deployment.

### Transformative Change Process

All steps above, plus:

1. Developer or ISSO completes a Security Impact Analysis (SIA) document [PLACEHOLDER — SIA template location].
2. SIA reviewed and signed by ISSO and ISO.
3. AO reviews SIA and provides written re-authorization before deployment.
4. SSP updated to reflect new system state within 30 days of deployment.

### Emergency Change Process

1. Emergency change implemented by Incident Commander with verbal AO approval (follow-up in writing within 24 hours).
2. Change documented in the Incident Report.
3. SIA completed within 5 business days.
4. AO provides written authorization within 5 business days.
5. Change log and SSP updated within 30 days.

---

## 5. Baseline Configuration Maintenance

The authorized baseline is the `main` branch of `wilcore-tech/demo-cato-system` as of the most recent ATO or re-authorization. The baseline is updated with each authorized change. Unauthorized deviations from baseline detected by automated scanning must be reported to the ISSO within 24 hours.

**Automated Drift Detection:** [PLACEHOLDER — describe drift detection tooling, e.g., AWS Config rules, Terraform plan in CI]

---

## 6. Document Maintenance

This plan is reviewed annually and updated to reflect changes to the change management process, tooling, or personnel. [PLACEHOLDER — document review history table].

---

*Document end.*
