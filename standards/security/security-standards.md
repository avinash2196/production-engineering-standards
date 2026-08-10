# Security Engineering Standard

## Purpose

Define mandatory security invariants for production software while keeping authentication, authorization, identity, encryption, and security products driven by approved requirements and architecture.

Security is mandatory. A specific security mechanism is not automatically mandatory merely because it is common in enterprise systems.

## Core Principle

Protect the actual trust boundaries, identities, resources, data, and dependencies established by the approved system design.

Do not invent:

- authentication requirements for deliberately public resources;
- an OAuth/OIDC provider;
- JWT algorithms or token formats;
- mTLS or workload identity;
- RBAC, ABAC, or another authorization model;
- HIPAA/PHI controls merely from healthcare vocabulary;
- encryption/key-management products;
- retention/audit requirements not established by policy or requirements.

When a material security decision is unresolved for the current Plan, ask the user rather than selecting a common default.

## Mandatory Invariants

### Trust Boundaries and Input Validation

Treat data crossing an external or lower-trust boundary as untrusted.

Validate applicable concerns such as:

- required fields and types;
- bounds and lengths;
- allowed values/formats;
- path/file safety;
- content type/size;
- injection risk;
- deserialization behavior;
- business invariants at the layer that owns them.

Transport validation must not replace domain/business validation when both are needed.

### Authentication

Protected resources must authenticate callers using the mechanism selected by the approved architecture.

Authentication may be unnecessary for explicitly public endpoints/resources. Do not add authentication merely because an endpoint exists.

When authentication is required:

- validate identity at the appropriate trust boundary;
- reject invalid/expired credentials correctly;
- avoid exposing credential details in errors/logs;
- do not implement custom cryptography or token verification when a supported platform/library exists.

Mechanisms may include OIDC/OAuth2, platform/workload identity, sessions, signed tokens, mTLS, API gateway identity, or other approved methods. This standard does not preselect one.

### Authorization

Authorization is required when authenticated identities have differing permissions or resource access.

Enforce authorization close enough to the protected operation that bypass is difficult.

The authorization model must follow approved requirements. Examples include:

- role-based access;
- attribute/policy-based access;
- resource ownership/tenant boundaries;
- service-to-service policy;
- delegated scopes/claims.

Do not infer RBAC/ABAC or PHI-specific authorization without requirements establishing that model.

### Least Privilege

Users, services, workloads, database accounts, and automation must receive only the permissions needed for their approved responsibilities.

Avoid broad wildcard permissions and shared privileged credentials unless explicitly justified and reviewed.

### Secrets and Credentials

Never commit secrets or credentials to source control.

Production credentials must come from an approved secure mechanism. Do not log secrets or include them in diagnostic responses.

Prefer short-lived or automatically rotated credentials when the approved platform supports them and the risk model justifies it.

### Secure Transport

Protect sensitive or authenticated traffic across untrusted or policy-defined network boundaries using the approved transport-security mechanism.

TLS may terminate at the application, ingress, proxy, service mesh, gateway, load balancer, or another approved boundary. Do not force application-level TLS when the platform already provides the required protection and trust model.

### Sensitive Data

Handle data according to the project's approved data classification.

At minimum:

- collect/store only data needed for the approved function;
- prevent sensitive values from leaking through logs, metrics, traces, errors, URLs, or debug endpoints;
- restrict access according to least privilege;
- use approved encryption/storage controls where the data classification requires them;
- avoid copying production sensitive data into local/test environments without an approved protection process.

Healthcare terminology does not by itself establish HIPAA applicability or that every health-related value is PHI. Apply HIPAA/PHI-specific controls only when project requirements, legal/compliance classification, or approved policy establishes them.

### Error Handling

External errors must not expose:

- stack traces;
- secrets;
- internal credentials;
- raw SQL;
- sensitive internal topology;
- sensitive payloads;
- authorization internals that meaningfully increase attackability.

Preserve enough internal diagnostic context through secure logs/telemetry without leaking it to untrusted callers.

### Data Access and Injection

Use parameterized database access and supported ORM/query APIs appropriately. Never compose untrusted values into executable SQL/shell/command/template contexts without safe binding or strict validation.

### Dependency and Supply-Chain Security

Production delivery should include dependency/source/image/security scanning appropriate to the adopting project and release environment.

Do not claim one scanner or remediation SLA as universal unless the organization has adopted it.

Material vulnerabilities must be assessed according to exploitability, exposure, data sensitivity, and approved risk policy.

### Security-Relevant Logging and Audit

Record security-relevant events when the approved threat/risk/compliance model requires them, while avoiding sensitive payload leakage.

Do not invent audit-retention durations or immutable-audit infrastructure unless requirements/policy establish them.

## Mechanism Selection

The following are design choices, not universal defaults:

- JWT vs sessions vs opaque tokens;
- RS256/ES256 vs platform-managed token verification;
- mTLS vs workload identity vs gateway identity;
- RBAC vs ABAC vs ownership/policy models;
- secret-manager vendor;
- KMS/key-management vendor;
- WAF/API gateway/service mesh;
- encryption-at-rest implementation;
- authentication middleware/framework.

Select them in the Plan/Implementation Plan from explicit requirements and repository-confirmed platform constraints.

## Local Development

Local development may use reduced-risk credentials/adapters when explicitly supported, but local mechanisms must never become an automatic production fallback.

Local configuration must not contain real production credentials or sensitive datasets.

## PDD Integration

Security is considered during requirements analysis and planning, but mechanisms are introduced only when sufficiently specified.

Examples:

- If a requirement says a resource is public, do not add authentication by convention.
- If a requirement says authenticated users have roles, authorization planning must resolve the role/resource behavior before implementation.
- If regulated data handling is explicitly established, planning must load the applicable compliance/privacy standards before code changes.

For behavior-changing security work, use separate RED and GREEN milestones. RED defines focused tests/checks for the approved security behavior; GREEN adds only the minimum implementation required. Refactor remains separate when justified.

## Review Questions

1. What are the trust boundaries?
2. Which resources are public versus protected?
3. How are callers identified, if identification is required?
4. What authorization decisions exist?
5. What data classification applies?
6. Which network/storage boundaries require encryption/protection?
7. What secrets/credentials exist and how are they provided?
8. What failure behavior prevents leakage or privilege escalation?
9. What security evidence is required for production release?

If an answer materially affects the current Plan and cannot be derived from explicit/repository-confirmed evidence, ask the user.

## Anti-Patterns

- Adding authentication to every endpoint by default.
- Selecting OAuth2/OIDC/JWT/mTLS because the service is called "enterprise".
- Treating RBAC or ABAC as universally required.
- Treating healthcare vocabulary as proof of HIPAA/PHI applicability.
- Logging request/response bodies containing sensitive data for troubleshooting.
- Hardcoding secrets or placing real credentials in example files.
- Writing custom cryptography when supported audited libraries/platform mechanisms exist.
- Granting broad service-account/database permissions for convenience.
- Declaring security complete because a framework security dependency was added.
