# Data Classification Template

Purpose
- Provide a lightweight data classification table to document sensitivity, retention, and handling rules for each data type used by the project.

Columns
- `data_type` | `sensitivity` (Public/PII/PHI/Restricted) | `access_controls` | `storage_encryption` | `retention` | `notes`

Fallback considerations
- Note whether local-adapter storage or local caches may contain sensitive data and how to secure or avoid such storage in dev.

Config & infra
- Config keys that control retention and encryption settings; infra components responsible for storage.

Validation
- Tests to assert redaction in logs and that sensitive data is not written to local fallback paths.
