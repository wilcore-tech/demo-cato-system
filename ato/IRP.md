# Incident Response Plan (IRP)
## NHLBI Research Data Portal (NHLBI-RDP)

**Document Version:** 1.2
**Classification:** FOR OFFICIAL USE ONLY (FOUO)
**Last Updated:** [PLACEHOLDER DATE]
**Next Review:** [PLACEHOLDER DATE]
**ISSO:** [PLACEHOLDER]

---

## 1. Purpose and Scope

This Incident Response Plan (IRP) establishes the procedures for detecting, reporting, analyzing, containing, eradicating, and recovering from security incidents affecting the NHLBI Research Data Portal (NHLBI-RDP). This plan is implemented in accordance with NIST SP 800-61 Rev 2 (Computer Security Incident Handling Guide) and satisfies NIST SP 800-53 Rev 5 IR family control requirements.

This plan applies to all personnel involved in the operation, maintenance, and use of NHLBI-RDP, including NIH staff, contractors, and authorized third parties.

---

## 2. Incident Response Team

| Role | Primary | Backup | Contact |
|---|---|---|---|
| Incident Commander | [PLACEHOLDER — ISSO] | [PLACEHOLDER — ISO] | [PLACEHOLDER — phone/email] |
| Technical Lead | [PLACEHOLDER — System Administrator] | [PLACEHOLDER] | [PLACEHOLDER] |
| Privacy Officer | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Communications Lead | [PLACEHOLDER — Mission Owner] | [PLACEHOLDER] | [PLACEHOLDER] |
| Legal/Counsel | NIH OGC | [PLACEHOLDER] | [PLACEHOLDER] |
| External Liaison (US-CERT) | Incident Commander | — | us-cert@hq.dhs.gov |

**Out-of-Hours Contact:** [PLACEHOLDER — on-call rotation or NOC number]

---

## 3. Incident Classification

| Category | Severity | Examples | Response Time |
|---|---|---|---|
| CAT 1 — Unauthorized Access | High/Critical | Successful intrusion, privilege escalation, unauthorized data exfiltration | Immediate (< 1 hour) |
| CAT 2 — Denial of Service | High | Service unavailability > 4 hours affecting research operations | < 2 hours |
| CAT 3 — Malicious Code | High | Ransomware, malware detected in production environment | < 1 hour |
| CAT 4 — Improper Usage | Medium | Policy violation by authorized user, data misuse | < 4 hours |
| CAT 5 — Scans/Probes | Low | Reconnaissance activity, failed brute-force attempts | < 24 hours |
| CAT 6 — Investigation | Informational | Anomalous activity requiring investigation but not confirmed incident | < 48 hours |

---

## 4. Incident Response Phases

### Phase 1 — Detection and Analysis

1. Security events are detected via AWS GuardDuty, CloudWatch Alarms, application audit logs, or user report.
2. The ISSO receives automated alert or report and performs initial triage within the response time window for the assessed category.
3. ISSO determines whether the event constitutes a confirmed incident or requires further investigation (CAT 6).
4. All analysis actions are documented in the Incident Tracking System: [PLACEHOLDER — ServiceNow/JIRA/other tool and project key].

**Evidence Preservation:** Prior to containment actions, capture: CloudWatch log streams, VPC Flow Logs for the incident window, ECS container logs, and AWS CloudTrail events. Preserve original evidence in [PLACEHOLDER — S3 bucket designated for incident evidence] with write-once (object lock) policy.

### Phase 2 — Containment

**Short-term containment options (choose based on incident type):**
- Isolate affected ECS task(s) by modifying security group rules to deny all inbound/outbound traffic
- Revoke compromised API keys or JWT signing keys via AWS Secrets Manager
- Disable affected user accounts in NIH Identity Management
- Block offending IP ranges at the ALB via WAF rule

**Long-term containment:** Deploy patched container image to production after validation in staging. Document all containment actions taken.

### Phase 3 — Eradication

1. Identify root cause of incident and confirm complete removal of threat.
2. For compromised container environments: terminate all running task instances and redeploy from a known-clean image.
3. For data integrity incidents: restore from last known-good Aurora snapshot and replay transaction logs to restore valid state.
4. Rotate all potentially exposed credentials (JWT keys, API keys, database passwords).

### Phase 4 — Recovery

1. Restore normal operations following the Contingency Plan (CP.md) procedures.
2. Validate system integrity: run automated test suite, verify audit log continuity, confirm security controls are operational.
3. Monitor system closely for 72 hours post-recovery for signs of re-compromise.
4. Document recovery timeline and actions.

### Phase 5 — Post-Incident Activity

1. Complete Incident Report (template: [PLACEHOLDER — link to template]) within 5 business days of incident closure.
2. Conduct post-incident review with all IRT members within 2 weeks.
3. Update POA&M with any new findings identified during incident.
4. Update this IRP if any gaps in procedures were identified.
5. Report to AO within 5 business days of closure.

---

## 5. Reporting Requirements

| Threshold | Report To | Timeline | Method |
|---|---|---|---|
| Any confirmed security incident | ISSO → ISO → AO | AO notification within 1 hour of confirmation | Phone + email |
| Any incident affecting PII or research data confidentiality | Privacy Officer + NIH Privacy Office | Within 1 hour of confirmation | Phone + email |
| CAT 1 or CAT 3 incidents | US-CERT (CISA) | Within 1 hour per US-CERT reporting guidelines | https://www.cisa.gov/report |
| HHS reportable incidents | HHS OCIO | Per HHS Incident Response Policy [PLACEHOLDER — policy reference] | HHS reporting portal |

---

## 6. Plan Testing and Maintenance

This plan is tested annually via a tabletop exercise. The last exercise was conducted on [PLACEHOLDER — exercise date] and the results are documented in [PLACEHOLDER — exercise report reference]. This plan is reviewed annually and after any significant incident or major system change.

---

*Document end.*
