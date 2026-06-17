# System Security Plan (SSP)
## NHLBI Research Data Portal (NHLBI-RDP)

**Document Version:** 1.4
**Classification:** FOR OFFICIAL USE ONLY (FOUO)
**Last Updated:** [PLACEHOLDER DATE]
**Next Scheduled Review:** [PLACEHOLDER DATE]

---

## Table of Contents

1. System Identification
2. Key Personnel
3. FIPS 199 Categorization
4. Authorization Boundary
5. External Integrations
6. Applicable Laws and Regulations
7. Security Control Narratives (NIST SP 800-53 Rev 5)

---

## 1. System Identification

| Field | Value |
|---|---|
| System Name | NHLBI Research Data Portal |
| System Abbreviation | NHLBI-RDP |
| System Identifier | NHLBI-RDP-001 |
| System Owner | [PLACEHOLDER — Mission Owner name and title] |
| System Type | Major Application |
| Operational Status | Operational |
| Environment | Production — AWS GovCloud (US-East-1) |
| FISMA Impact Level | Moderate |
| Authorization Boundary | See Section 4 |
| System Description | Web-based portal providing authenticated, role-based access to de-identified clinical research datasets maintained by NHLBI. The portal enforces data use agreement (DUA) terms and provides audit logging for all data access events. |

---

## 2. Key Personnel

| Role | Name | Organization | Phone | Email |
|---|---|---|---|---|
| Mission Owner (MO) | [PLACEHOLDER] | NHLBI | [PLACEHOLDER] | [PLACEHOLDER] |
| Authorizing Official (AO) | [PLACEHOLDER] | NIH OCIO | [PLACEHOLDER] | [PLACEHOLDER] |
| AO Designated Representative (AODR) | [PLACEHOLDER] | NIH OCIO | [PLACEHOLDER] | [PLACEHOLDER] |
| Information System Owner (ISO) | [PLACEHOLDER] | NHLBI | [PLACEHOLDER] | [PLACEHOLDER] |
| Information System Security Officer (ISSO) | [PLACEHOLDER] | NHLBI | [PLACEHOLDER] | [PLACEHOLDER] |
| System Administrator | [PLACEHOLDER] | [PLACEHOLDER — contractor or FTE] | [PLACEHOLDER] | [PLACEHOLDER] |
| Database Administrator | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Privacy Officer | [PLACEHOLDER] | NIH OPDIV Privacy Office | [PLACEHOLDER] | [PLACEHOLDER] |

---

## 3. FIPS 199 Categorization

Security categorization performed per FIPS Publication 199 and NIST SP 800-60 Vol. II.

| Security Objective | Impact Level | Rationale |
|---|---|---|
| Confidentiality | **Moderate** | System holds de-identified research data. Re-identification risk exists if combined with external datasets. Loss of confidentiality could cause reputational harm and researcher trust erosion, but no direct harm to research subjects per current data use agreements. |
| Integrity | **Moderate** | Corruption or unauthorized modification of research datasets could compromise study validity and downstream publications. Integrity failures are detectable through checksums and audit logging. |
| Availability | **Low** | System supports research workflows with no real-time clinical dependency. Outages lasting up to 72 hours are acceptable per business impact analysis. |
| **Overall System Categorization** | **MODERATE** | Determined by the high-water mark of individual objectives. |

---

## 4. Authorization Boundary

The NHLBI-RDP authorization boundary encompasses:

- **Application Layer:** FastAPI application containers running on AWS ECS Fargate in a dedicated VPC (CIDR: 10.10.0.0/16). Containers are isolated in private subnets with no direct internet ingress.
- **Data Layer:** PostgreSQL-compatible Amazon Aurora cluster in isolated private subnets. All data at rest encrypted using AES-256 (AWS KMS).
- **Ingress Layer:** AWS Application Load Balancer (ALB) accepting only TLS 1.2/1.3 on port 443 from the public internet. All HTTP traffic rejected.
- **CI/CD Pipeline:** GitHub Actions runners operating in ephemeral environments. Pipeline artifacts (container images) stored in Amazon ECR.
- **Secrets Management:** AWS Secrets Manager for runtime secrets injection. No secrets stored in environment variables or source code.

**Out of Scope:**
- NIH enterprise identity provider (IdP) — governed by separate NIH-OCIO ATO
- NCBI upstream data APIs — governed by NCBI system boundary
- End-user workstations and network infrastructure

---

## 5. External Integrations

| System | Owner | Connection Type | Data Exchanged | Agreement | Direction |
|---|---|---|---|---|---|
| NIH Enterprise IdP | NIH OCIO | SAML 2.0 over HTTPS | Authentication assertions only | ISA-NIH-OCIO-2024-001 [PLACEHOLDER — agreement number] | Inbound (auth only) |
| NCBI Entrez API | NLM/NCBI | REST over HTTPS | Dataset metadata (read-only) | MOU-NHLBI-NCBI-2024-003 [PLACEHOLDER] | Outbound |
| AWS CloudTrail/CloudWatch | AWS (FedRAMP Moderate) | Internal AWS API | System and audit logs | N/A (AWS service) | Outbound |
| NIH Enterprise Email (SMTP) | NIH OCIO | SMTP/TLS | Notification emails (no PII) | MOU-NHLBI-OCIO-EMAIL [PLACEHOLDER] | Outbound |

---

## 6. Applicable Laws and Regulations

- Federal Information Security Modernization Act (FISMA), 44 U.S.C. § 3551 et seq.
- OMB Circular A-130, Managing Information as a Strategic Resource (2016)
- NIST SP 800-53 Rev 5, Security and Privacy Controls for Information Systems and Organizations
- NIST SP 800-37 Rev 2, Risk Management Framework for Information Systems
- NIST SP 800-60 Vol. II, Guide for Mapping Types of Information and Information Systems to Security Categories
- FIPS 140-3, Security Requirements for Cryptographic Modules
- FIPS 199, Standards for Security Categorization of Federal Information and Information Systems
- Health Insurance Portability and Accountability Act (HIPAA) — Note: System holds de-identified data; HIPAA applicability reviewed in PIA [PLACEHOLDER — confirm HIPAA applicability status]
- NIH Information Security and Privacy Program policies
- NIH HHS System of Records Notice (SORN) [PLACEHOLDER — applicable SORN identifier]

---

## 7. Security Control Narratives

*Controls are organized by NIST SP 800-53 Rev 5 control families. Each narrative describes how the control is implemented for NHLBI-RDP. Controls marked `[CURRENT — last updated: PLACEHOLDER DATE]` require date updates during each annual review.*

---

### AC — Access Control

`[CURRENT — last updated: PLACEHOLDER DATE]`

**AC-1 (Policy and Procedures):** NHLBI-RDP access control policy is documented in this SSP and the Configuration Management Plan. Access privileges are reviewed quarterly by the ISSO and Mission Owner. The policy is reviewed annually and upon significant change.

**AC-2 (Account Management):** User accounts are provisioned through the NIH Identity Management system. Researchers must submit a Data Access Request (DAR) approved by the Data Access Committee (DAC) before accounts are created. Accounts are reviewed every 90 days and disabled immediately upon role change or separation. Privileged accounts (system administrators) are enumerated in the [PLACEHOLDER — privileged account registry document].

**AC-3 (Access Enforcement):** Role-based access control (RBAC) is implemented at the application layer. Three roles are defined: `researcher` (read-only dataset access), `data_steward` (dataset management), and `admin` (system administration). Access enforcement is implemented in the FastAPI authorization middleware and enforced at the database layer via row-level security.

**AC-6 (Least Privilege):** All AWS IAM roles follow least-privilege principles. The ECS task role (`nhlbi-rdp-app-task`) is limited to S3 read access on the datasets bucket and CloudWatch Logs write access. Administrative access to AWS infrastructure requires separate Just-in-Time (JIT) privileged access managed through [PLACEHOLDER — PAM tool name].

**AC-7 (Unsuccessful Logon Attempts):** The system enforces account lockout after 3 consecutive failed authentication attempts. Locked accounts are released after 30 minutes or by ISSO action. Lockout events are logged and generate automated alerts to the ISSO.

**AC-12 (Session Termination):** Sessions expire after 30 minutes of inactivity. The system locks the session after 15 minutes of idle time, requiring re-authentication. Concurrent session limit is set to 1 per user account.

---

### AU — Audit and Accountability

`[CURRENT — last updated: PLACEHOLDER DATE]`

**AU-2 (Event Logging):** The following events are logged: authentication successes and failures, account management actions, dataset access (read), privilege escalation attempts, configuration changes, and system errors. Log format: structured JSON with timestamp, user_id, action, resource, IP address, and outcome.

**AU-3 (Content of Audit Records):** Each audit record includes: (1) date and time of the event (UTC); (2) user or process identifier; (3) type of event; (4) resource accessed; (5) source IP address; (6) outcome (success/failure); (7) additional context in JSONB field.

**AU-9 (Protection of Audit Information):** Audit logs are written to an immutable `audit_log` table with a database-level rule preventing deletion (`CREATE RULE no_delete_audit`). Logs are also streamed to AWS CloudWatch Logs, which is configured with a 7-year retention period and write-once (no-delete) policy enforced by CloudWatch resource policy. Only the ISSO and designated security personnel have read access to audit logs.

**AU-11 (Audit Record Retention):** Audit records are retained for 7 years per NIH Records Schedule N1-443-11-001 [PLACEHOLDER — verify applicable records schedule].

**AU-12 (Audit Record Generation):** All application components generate audit records. The database layer generates records for all DML operations on sensitive tables. Infrastructure-level audit records are generated by AWS CloudTrail (management events) and VPC Flow Logs (network events).

---

### CM — Configuration Management

`[CURRENT — last updated: PLACEHOLDER DATE]`

**CM-2 (Baseline Configuration):** The authorized baseline configuration for NHLBI-RDP is maintained in the GitHub repository `wilcore-tech/demo-cato-system` (main branch). All configuration is defined as code (Infrastructure as Code via Terraform, container images via Dockerfile, Kubernetes manifests). The baseline is reviewed and updated with each authorized change.

**CM-3 (Configuration Change Control):** All changes to the system baseline follow the change management process defined in the Configuration Management Plan (CMP). Changes are classified as Routine Recurring, Adaptive, Transformative, or Emergency per the cATO change classification framework. Transformative changes require AO re-authorization. Change requests are tracked in [PLACEHOLDER — ticketing system and project].

**CM-6 (Configuration Settings):** Security-relevant configuration settings are defined in `app/src/auth/config.py` (authentication policy), Terraform modules (infrastructure settings), and Kubernetes manifests (container runtime settings). All containers run as non-root (UID 1000), with read-only root filesystems and dropped Linux capabilities.

**CM-7 (Least Functionality):** The system disables all unnecessary ports, protocols, and services. The container exposes only port 8080 (internal). The ALB accepts only port 443 (TLS). FastAPI documentation endpoints (Swagger UI, ReDoc) are disabled in production. SSH access to containers is not permitted; all administrative access is through AWS ECS Exec with audit logging.

**CM-8 (System Component Inventory):** Component inventory is maintained automatically through Terraform state (infrastructure) and GitHub Packages (container images with SBOMs). The ISSO reviews the inventory quarterly. [PLACEHOLDER — link to inventory artifact or process].

---

### IA — Identification and Authentication

`[CURRENT — last updated: PLACEHOLDER DATE]`

**IA-2 (Identification and Authentication — Organizational Users):** All organizational users authenticate through the NIH Enterprise Identity Provider (IdP) using SAML 2.0. Direct username/password authentication to NHLBI-RDP is not permitted for organizational users. The system does not store user passwords.

**IA-3 (Device Identification and Authentication):** Service-to-service authentication uses mutual TLS (mTLS) for internal API calls. External integrations use API keys stored in AWS Secrets Manager, rotated every 90 days. [PLACEHOLDER — describe any device certificates in use].

**IA-5 (Authenticator Management):** Authentication is delegated to NIH IdP (see IA-2). For API key authenticators managed by NHLBI-RDP: minimum length 32 characters, cryptographically random, rotated every 90 days, stored in AWS Secrets Manager with rotation lambda configured.

**IA-8 (Identification and Authentication — Non-Organizational Users):** Non-NIH researchers authenticate via NIH eRA Commons federated login through the same SAML 2.0 flow. [PLACEHOLDER — confirm eRA Commons integration is in scope or document as separate ISA].

---

### SC — System and Communications Protection

`[CURRENT — last updated: PLACEHOLDER DATE]`

**SC-5 (Denial of Service Protection):** AWS Shield Standard is enabled on the ALB. Rate limiting is configured at the ALB (1,000 requests/minute per IP) and at the application layer (100 requests/minute per authenticated user). [PLACEHOLDER — confirm AWS Shield Advanced subscription if required for Moderate systems under current NIH policy].

**SC-8 (Transmission Confidentiality and Integrity):** All data in transit is encrypted using TLS 1.2 or TLS 1.3. TLS 1.0 and 1.1 are explicitly disabled. The ALB SSL policy is `ELBSecurityPolicy-TLS13-1-2-2021-06`. All external API client calls enforce `verify=True` (TLS certificate validation). Internal service communication within the VPC uses TLS where supported by the service.

**SC-12 (Cryptographic Key Establishment and Management):** Cryptographic keys are managed through AWS KMS. Data encryption keys (DEKs) for S3 and Aurora are managed by KMS customer-managed keys (CMKs) with automatic annual rotation. JWT signing keys are RSA-2048, stored in AWS Secrets Manager, rotated every 365 days.

**SC-28 (Protection of Information at Rest):** All data at rest is encrypted: Aurora database uses AES-256 with KMS CMK; S3 dataset bucket uses SSE-KMS with CMK; EBS volumes (Fargate ephemeral storage) use AES-256 encryption. Encryption keys are managed per SC-12.

---

### SA — System and Services Acquisition

`[CURRENT — last updated: PLACEHOLDER DATE]`

**SA-3 (System Development Life Cycle):** NHLBI-RDP follows a DevSecOps SDLC. Security is integrated at each phase: design (threat modeling), development (SAST via ruff and Bandit), build (container image scanning via Trivy), and deployment (IaC security scanning via Checkov). All code changes are reviewed via pull request with mandatory security review for changes affecting security-relevant files.

**SA-8 (Security and Privacy Engineering Principles):** The system is designed with the following principles: defense in depth (multiple security layers), least privilege (IAM and RBAC), separation of duties (no single individual controls end-to-end deployment), fail secure (authentication failures deny access by default), and economy of mechanism (minimal attack surface).

**SA-10 (Developer Configuration Management):** All source code is version-controlled in GitHub. Branch protection rules require pull request reviews before merging to main. Signed commits are [PLACEHOLDER — enabled/not yet enabled — document status]. Dependency updates are automated via Dependabot with mandatory review.

**SA-11 (Developer Testing and Evaluation):** Automated testing includes: unit tests (pytest), dependency vulnerability scanning (Trivy, run in CI on every PR), and static analysis (ruff). Security testing results are reviewed by the ISSO for each release. Penetration testing is conducted annually by [PLACEHOLDER — third-party assessor name].

---

### SI — System and Information Integrity

`[CURRENT — last updated: PLACEHOLDER DATE]`

**SI-2 (Flaw Remediation):** Vulnerability scanning is performed by Trivy in the CI pipeline on every pull request and weekly on the main branch image. Critical and High CVEs fail the build and block deployment. Patch timelines: Critical — 72 hours; High — 30 days; Medium — 90 days. Patch status is tracked in the POA&M.

**SI-3 (Malicious Code Protection):** Container images are scanned for malware signatures by Trivy at build time. Runtime protection is provided by [PLACEHOLDER — runtime security tool, e.g., Falco, Amazon GuardDuty]. Container immutability (read-only root filesystem) prevents runtime injection.

**SI-4 (System Monitoring):** The system is monitored by AWS CloudWatch (metrics and alarms), AWS GuardDuty (threat detection), and VPC Flow Logs (network traffic). Alerts are configured for: authentication failures exceeding threshold, unusual API call patterns, new IAM activity, and container restarts. Alerts route to the ISSO via [PLACEHOLDER — SIEM or alerting tool].

**SI-7 (Software, Firmware, and Information Integrity):** Container images are signed using [PLACEHOLDER — Cosign/Notary — document signing approach]. SBOMs are generated at build time and stored with each container image. Terraform state integrity is enforced by S3 versioning and DynamoDB state locking.

---

### SR — Supply Chain Risk Management

`[CURRENT — last updated: PLACEHOLDER DATE]`

**SR-2 (Supply Chain Risk Management Plan):** NHLBI-RDP's supply chain risk management approach is integrated into the DevSecOps pipeline. All open-source dependencies are tracked via SBOM (generated by Syft at build time). Dependencies are reviewed for known vulnerabilities before any version update is merged.

**SR-3 (Supply Chain Controls and Plans):** Controls include: (1) dependency pinning — all package versions pinned in `requirements.txt`; (2) automated vulnerability scanning — Trivy scans on every PR; (3) container base image provenance — images pulled only from verified registries (Docker Hub official, PyPI); (4) CI runner integrity — GitHub Actions uses pinned action versions with SHA digests where feasible.

**SR-11 (Component Authenticity):** Software components are verified against package registry checksums (pip hash verification). Container images are verified by digest before deployment. [PLACEHOLDER — document any additional component verification procedures].

---

### Additional Control Families (Summary)

The following control families are implemented with narratives maintained in the attached control matrix spreadsheet [PLACEHOLDER — link to control matrix]:

| Family | Status |
|---|---|
| AT — Awareness and Training | Implemented — NIH enterprise training program |
| CA — Assessment, Authorization, and Monitoring | Implemented — see ATO Letter and SAR |
| CP — Contingency Planning | Implemented — see CP.md |
| IR — Incident Response | Implemented — see IRP.md |
| MA — Maintenance | Implemented — [PLACEHOLDER — maintenance procedures] |
| MP — Media Protection | Implemented — no removable media; AWS encryption |
| PE — Physical and Environmental | Inherited — AWS GovCloud physical controls |
| PL — Planning | Implemented — this SSP |
| PM — Program Management | Inherited — NIH enterprise ISMS |
| PS — Personnel Security | Implemented — NIH HR and background check procedures |
| PT — PII Processing and Transparency | Implemented — see PIA.md and PTA.md |
| RA — Risk Assessment | Implemented — annual RA, last completed [PLACEHOLDER] |

---

## Approval and Signature Block

| Role | Name | Signature | Date |
|---|---|---|---|
| Information System Security Officer | [PLACEHOLDER] | _________________ | [PLACEHOLDER] |
| Information System Owner | [PLACEHOLDER] | _________________ | [PLACEHOLDER] |
| Mission Owner | [PLACEHOLDER] | _________________ | [PLACEHOLDER] |
| Authorizing Official | [PLACEHOLDER] | _________________ | [PLACEHOLDER] |

---

*Document end. Version history maintained in GitHub repository.*