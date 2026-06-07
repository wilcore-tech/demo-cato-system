# Contingency Plan (CP)
## NHLBI Research Data Portal (NHLBI-RDP)

**Document Version:** 1.1
**Classification:** FOR OFFICIAL USE ONLY (FOUO)
**Last Updated:** [PLACEHOLDER DATE]
**Next Review:** [PLACEHOLDER DATE]
**ISSO:** [PLACEHOLDER]

---

## 1. Purpose and Scope

This Contingency Plan (CP) establishes recovery procedures for NHLBI-RDP to ensure continuity of operations following disruption, degradation, or failure of system components. This plan is implemented per NIST SP 800-34 Rev 1 (Contingency Planning Guide for Federal Information Systems) and satisfies CP family controls under NIST SP 800-53 Rev 5.

**System Recovery Objectives:**

| Metric | Target | Rationale |
|---|---|---|
| Recovery Time Objective (RTO) | 72 hours | System supports non-time-critical research workflows. No real-time clinical dependency. |
| Recovery Point Objective (RPO) | 24 hours | Daily Aurora snapshots are sufficient; dataset files are immutable. |
| Maximum Tolerable Downtime (MTD) | 7 days | Researchers can buffer work for up to one week without significant impact. |

---

## 2. Contingency Planning Team

| Role | Name | Contact | Responsibility |
|---|---|---|---|
| Contingency Plan Coordinator | [PLACEHOLDER — ISSO] | [PLACEHOLDER] | Overall CP execution, AO notification |
| Technical Recovery Lead | [PLACEHOLDER — System Administrator] | [PLACEHOLDER] | Infrastructure recovery |
| Database Recovery Lead | [PLACEHOLDER — DBA] | [PLACEHOLDER] | Data restoration |
| Mission Owner | [PLACEHOLDER] | [PLACEHOLDER] | Business decisions, user communications |
| AWS Support Contact | AWS Enterprise Support | [PLACEHOLDER — support PIN] | AWS infrastructure assistance |

---

## 3. System Backup and Recovery Configuration

**Database (Aurora PostgreSQL):**
- Automated daily snapshots retained for 35 days
- Point-in-time recovery (PITR) enabled — recovery to any point within 35 days
- Snapshots stored in S3 (same region) with cross-region copy to `us-west-2` [PLACEHOLDER — confirm cross-region replication is configured]
- Snapshot restoration tested quarterly [PLACEHOLDER — last test date]

**Dataset Files (S3):**
- S3 versioning enabled on `nhlbi-rdp-datasets` bucket
- Cross-region replication to `us-west-2` with 15-minute replication SLA
- S3 Object Lock (WORM) applied to finalized dataset objects

**Container Images (ECR):**
- All production images tagged and retained in ECR
- Image digests recorded in deployment manifest for each release
- Last known-good image: [PLACEHOLDER — record after each production deployment]

**Secrets (AWS Secrets Manager):**
- Secrets backed up via [PLACEHOLDER — describe backup procedure or confirm AWS durability is sufficient]
- Secret version history retained for 30 days

**Terraform State:**
- State stored in S3 with versioning enabled
- State lock via DynamoDB

---

## 4. Recovery Procedures

### Scenario A — Application Container Failure

1. AWS ECS service auto-recovery will attempt to restart failed tasks automatically.
2. If auto-recovery fails, ISSO/SysAdmin manually triggers ECS service redeployment via AWS Console or CLI.
3. Validate health check endpoint (`GET /health`) returns 200 OK.
4. Estimated recovery time: < 15 minutes for single container failure.

### Scenario B — Database Failure

1. Aurora Multi-AZ configuration provides automatic failover to standby replica (typically < 30 seconds).
2. For data corruption scenarios: identify last clean restore point in AWS Console → RDS → Automated Backups.
3. Restore to new Aurora cluster from snapshot; update application connection string (SSM Parameter Store).
4. Validate data integrity via checksum verification on key dataset tables.
5. Estimated recovery time: 2–4 hours for full snapshot restore.

### Scenario C — AWS Region Failure (us-east-1)

1. Declare regional disaster; notify AO within 1 hour.
2. Initiate recovery to `us-west-2` (disaster recovery region).
3. Restore Aurora from cross-region snapshot.
4. Redeploy ECS service in DR VPC (pre-provisioned via Terraform in `us-west-2`).
5. Update Route 53 DNS to point to DR ALB. [PLACEHOLDER — confirm DR Terraform configuration exists]
6. Notify users of temporary reduced capacity.
7. Estimated recovery time: 24–48 hours; within RTO of 72 hours.

### Scenario D — Ransomware or Destructive Attack

1. Follow IRP Phase 1–3 (Detection, Containment, Eradication) before recovery.
2. Do not restore from backups until eradication is confirmed.
3. Provision clean infrastructure from Terraform (destroy and re-apply in isolated account if necessary).
4. Restore from last clean pre-incident snapshot identified via forensic timeline.
5. Coordinate with US-CERT as required by IRP.

---

## 5. Plan Testing and Maintenance

| Activity | Frequency | Last Completed | Next Scheduled |
|---|---|---|---|
| Tabletop exercise | Annual | [PLACEHOLDER] | [PLACEHOLDER] |
| Database restore test | Quarterly | [PLACEHOLDER] | [PLACEHOLDER] |
| Failover test (Aurora Multi-AZ) | Annual | [PLACEHOLDER] | [PLACEHOLDER] |
| Cross-region recovery drill | Annual | [PLACEHOLDER] | [PLACEHOLDER] |

This plan is reviewed annually and updated after each test or significant system change. Test results are documented in [PLACEHOLDER — test report location].

---

*Document end.*
