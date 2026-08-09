# Audit Logging

## Purpose

Define the audit logging schema, immutability requirements, retention policies, and implementation patterns for tracking access to and modification of classified data. Audit logs are distinct from application/operational logs — they serve compliance, security investigation, and accountability purposes.

## When Audit Logging Is Required

| Data Classification | Create | Read | Update | Delete |
|--------------------|--------|------|--------|--------|
| Public | No | No | No | No |
| Internal | No | No | Optional | Optional |
| Confidential | Yes | Optional | Yes | Yes |
| Restricted / PHI | Yes | Yes | Yes | Yes |

Reference: `data-classification.md` for classification definitions.

## Audit Event Schema

Every audit event must include these fields:

```json
{
  "eventId": "uuid-v4",
  "eventType": "DATA_ACCESS | DATA_CREATE | DATA_UPDATE | DATA_DELETE",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "actor": {
    "type": "USER | SERVICE | SYSTEM",
    "id": "user-123 | order-service",
    "ip": "10.0.1.15",
    "roles": ["clinician", "admin"]
  },
  "resource": {
    "type": "patient | order | document",
    "id": "patient-456",
    "classification": "RESTRICTED"
  },
  "action": {
    "operation": "READ",
    "fields": ["name", "dob", "diagnosis"],
    "query": "GET /api/patients/456"
  },
  "outcome": {
    "status": "SUCCESS | FAILURE | DENIED",
    "reason": "null | insufficient_permissions | resource_not_found"
  },
  "context": {
    "traceId": "abc-123",
    "correlationId": "req-789",
    "service": "patient-service",
    "environment": "production"
  }
}
```

### Schema Rules

- **`eventId`** must be a globally unique identifier (UUID v4).
- **`actor.id`** must be the authenticated identity. Never use "anonymous" or "system" for PHI access.
- **`resource.id`** is the record identifier. Never include the actual PHI values in the audit event.
- **`action.fields`** lists which fields were accessed or modified. For updates, include old and new values only if the values are not PHI — otherwise log field names only.
- **`outcome.status`** must always be present, including for denied access attempts.

## Immutability Requirements

Audit logs must be tamper-resistant once written:

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| Append-only storage | Write-once storage (S3 Object Lock, Azure Immutable Blob) | Default for all compliance-grade audit logs |
| Separate write permissions | Audit log storage is writable only by the audit service; application services cannot modify or delete | Always |
| Cryptographic chaining | Each event includes a hash of the previous event | High-security environments |
| External witness | Audit events forwarded to an external SIEM in real-time | When breach detection is required |

**Mandatory rules:**
- Application services must not have delete or update permissions on audit log storage.
- Audit logs must be written synchronously or with at-most-once-delayed guarantees (buffer ≤ 5 seconds before flush).
- Failed audit writes must not fail the business operation silently — emit an alert metric.

## Retention Policy

Audit retention is defined by applicable legal, regulatory, contractual, and organizational policy for the system and data involved. HIPAA's six-year documentation-retention requirement must not be treated as a universal six-year rule for every application audit log or medical record.

- Record the policy/source that determines retention for each audit stream.
- Enforce approved retention through storage lifecycle controls where practical.
- Protect records for the full retention period and use an approved disposal mechanism afterward.
- Keep legal holds and investigation requirements separate from normal lifecycle deletion.

## Implementation Patterns

### Java (Spring)

```java
@Component
public class AuditLogger {
    private final AuditEventStore store;

    public void logAccess(AuditEvent event) {
        event.setEventId(UUID.randomUUID().toString());
        event.setTimestamp(Instant.now());
        store.append(event);
        meterRegistry.counter("audit_events_total",
            "type", event.getEventType(),
            "classification", event.getResource().getClassification()
        ).increment();
    }
}

// Usage in service layer
public PatientDto getPatient(String patientId, AuthContext auth) {
    Patient patient = patientRepository.findById(patientId);
    auditLogger.logAccess(AuditEvent.builder()
        .eventType("DATA_ACCESS")
        .actor(auth.toActor())
        .resource(AuditResource.of("patient", patientId, "RESTRICTED"))
        .action(AuditAction.read("name", "dob", "diagnosis"))
        .outcome(AuditOutcome.success())
        .context(AuditContext.fromTrace())
        .build());
    return PatientDto.from(patient);
}
```

### Python (FastAPI)

```python
class AuditLogger:
    def __init__(self, store: AuditEventStore):
        self.store = store

    def log_access(self, event: AuditEvent) -> None:
        event.event_id = str(uuid4())
        event.timestamp = datetime.utcnow()
        self.store.append(event)

# Usage in endpoint
@router.get("/patients/{patient_id}")
async def get_patient(patient_id: str, auth: AuthContext = Depends(get_auth)):
    patient = await patient_repo.find_by_id(patient_id)
    audit_logger.log_access(AuditEvent(
        event_type="DATA_ACCESS",
        actor=auth.to_actor(),
        resource=AuditResource(type="patient", id=patient_id, classification="RESTRICTED"),
        action=AuditAction.read(fields=["name", "dob", "diagnosis"]),
        outcome=AuditOutcome.success(),
    ))
    return PatientDto.from_entity(patient)
```

## What NOT to Audit Log

- Operational events (service startup, health checks, config changes) → use application logs.
- Performance metrics → use metrics/tracing.
- Debug information → use application logs at DEBUG level.
- Raw PHI values → log resource IDs and field names only.

## Alerting

Configure alerts for:

| Condition | Severity | Response |
|-----------|----------|----------|
| Bulk PHI access (> N records in M minutes by one actor) | High | Investigate for data exfiltration |
| Access denied to restricted resources | Medium | Review for privilege escalation attempts |
| Audit write failures | Critical | Audit pipeline is broken — fix immediately |
| Access from unusual IP/service | Medium | Verify legitimacy |

## LLM Instructions

- When generating code that accesses Confidential or Restricted data, include audit logging calls.
- Use the audit event schema above — do not invent a different format.
- Never include raw PHI in audit events — use resource IDs and field names.
- Place audit logging in the service layer, after the data operation, before returning to the caller.
- Ask the user about retention requirements if generating audit infrastructure.

## Review Checklist

- [ ] Audit events emitted for all required CRUD operations per data classification.
- [ ] Audit event schema matches the standard (eventId, actor, resource, action, outcome, context).
- [ ] No raw PHI or secret values in audit events.
- [ ] Audit storage is append-only or write-once.
- [ ] Application services cannot delete or modify audit logs.
- [ ] Retention policy configured and automated.
- [ ] Alert rules configured for anomalous access patterns.
- [ ] Audit write failures produce alerts, not silent failures.
