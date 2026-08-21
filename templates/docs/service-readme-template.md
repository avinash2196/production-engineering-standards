# <Service Name>

Briefly describe the service's purpose and the business capability it provides.

## Responsibilities

- <responsibility>

## Interfaces

Document only interfaces that actually exist.

| Interface | Direction | Purpose | Contract |
|---|---|---|---|
| <HTTP/event/job> | <inbound/outbound> | <purpose> | <link or description> |

## Runtime and Dependencies

List the selected runtime and only the external dependencies the service actually uses.

| Dependency | Purpose | Failure behavior |
|---|---|---|
| <dependency> | <purpose> | <fail/retry/degrade behavior> |

## Configuration

Document required configuration, defaults that are intentionally safe, and any production guards. Do not include real secrets.

## Local Development

Describe the smallest supported local setup, including any explicitly selected local adapters or emulators and their reduced guarantees.

## Build and Test

```bash
<build command>
<test command>
```

## Observability and Operations

Document the logging, metrics, tracing, health, alerting, and operational behavior that the service actually implements and operators need.

## Security and Data Handling

Document trust boundaries, authentication/authorization where applicable, data classification, and secret handling based on approved project requirements.

## Known Limitations

- <limitation or none>

## References

- <design/ADR/API/standard links>
