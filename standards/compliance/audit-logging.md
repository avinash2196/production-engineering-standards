# Audit Logging

## Purpose

Define engineering principles for audit evidence when an approved security, compliance, contractual, or business policy requires accountable records of sensitive actions. Audit logs are distinct from ordinary diagnostic/application logs.

## Applicability

Do not audit every CRUD operation merely because this document exists. Establish:

- which actions/resources require audit evidence;
- who/what must be attributable;
- what outcomes/context must be recorded;
- integrity/availability requirements;
- retention/disposal source;
- monitoring/review obligations.

These decisions come from the applicable policy, threat/risk assessment, or business requirement.

## Event Content

An audit event normally needs enough information to answer questions such as:

- **who/what** performed or attempted the action;
- **what** action occurred;
- **which resource/data scope** was affected;
- **when** it occurred;
- **outcome** (success, failure, denied);
- **useful request/operation context** for investigation.

A project may use a schema like:

```json
{
  "eventId": "<globally-unique-id>",
  "eventType": "DATA_ACCESS",
  "timestamp": "<timestamp>",
  "actor": {"type": "USER_OR_SERVICE", "id": "<identity>"},
  "resource": {"type": "<type>", "id": "<identifier>", "classification": "<approved-label>"},
  "action": {"operation": "READ"},
  "outcome": {"status": "SUCCESS"},
  "context": {"traceOrRequestId": "<optional-context>"}
}
```

The shape is illustrative unless the adopting organization explicitly adopts it as its audit schema. A globally unique event identifier need not be UUID v4 specifically.

## Sensitive Data

- Record identifiers/field names rather than raw sensitive values whenever possible.
- Never place secrets in audit events.
- Minimize personal/sensitive information in audit records to what the audit purpose requires.
- Protect audit data itself according to its classification and access needs.

## Integrity and Availability

Use controls appropriate to the approved audit requirement, such as restricted append access, immutable/write-once storage, separation of duties, external forwarding/SIEM, cryptographic integrity, or provider-native audit services.

This repository does not impose one storage technology or a universal synchronous/5-second flush requirement. Define loss/delay guarantees from the actual policy and failure model. Audit pipeline failures that threaten a required control must be observable and handled according to the approved design.

## Retention and Disposal

Retention is determined by applicable law/regulation, contract, records policy, security policy, and investigation/legal-hold requirements. Record the source for each required retention period and implement approved lifecycle/disposal controls.

Do not infer that HIPAA imposes one universal application-audit-log or medical-record retention duration.

## Placement and Failure Semantics

Choose where audit emission occurs so bypass is difficult and the record corresponds to the authoritative action/outcome. Depending on the architecture this can be application/service logic, database/platform audit, gateway/policy layer, an event stream, or a dedicated audit service.

Define what happens if required audit recording fails. Some operations may fail closed; others may use a durable asynchronous path. The decision must come from policy and business correctness requirements.

## Alerting / Review

Where required, monitor for audit-pipeline failure and suspicious access patterns. Thresholds/severity/response procedures are system- and organization-specific; do not invent universal numeric triggers.

## LLM Instructions

- Confirm that audit logging is required for the reviewed action before adding it.
- Derive event fields, durability, retention, and failure behavior from the approved policy/design.
- Never log raw secrets or unnecessary sensitive values.
- Do not hard-code UUID version, storage technology, flush latency, or retention period without evidence.
- Distinguish diagnostic logs from compliance/security audit records.

## Review Checklist

- [ ] Audit applicability and policy source are documented.
- [ ] Required actor/action/resource/time/outcome context is available.
- [ ] Audit records avoid raw secrets and unnecessary sensitive values.
- [ ] Integrity/access/durability controls satisfy the stated requirement.
- [ ] Required audit-write failures are observable and have explicit behavior.
- [ ] Retention/disposal has an identified policy source.
