# Transport Protection

## Purpose

Define engineering outcomes for protecting network traffic without hard-coding a transport topology, TLS termination point, cipher list, mTLS requirement, or protocol version that may belong to organization/platform security policy.

The canonical security policy is [Security Engineering Standard](security-standards.md).

## Applicability

Protect traffic when confidentiality, integrity, authenticated identity, regulatory policy, or the network trust model requires it. Public, authenticated, internal, database, broker, cache, and secret-store flows can have different controls based on the approved architecture.

Do not assume that every service must terminate TLS itself. Protection may be provided by an ingress, gateway, load balancer, service mesh, managed service, application server, or another approved boundary.

## Required Outcomes

When transport protection is required:

- use protocols/cipher configuration allowed by the organization's current security baseline and target platform;
- validate peer/server identity according to the chosen trust model;
- keep private keys and certificate credentials out of source control and ordinary logs;
- automate or operationalize certificate/key renewal according to the platform mechanism;
- fail safely when required transport identity/protection cannot be established;
- verify that hops outside the protected boundary are not accidentally sent in clear text;
- test the deployed configuration rather than inferring security from application dependencies alone.

## Mutual Authentication

mTLS is one possible service-to-service identity/protection mechanism. Require it only when the approved architecture/security policy selects it. Other valid models can include workload identity, signed requests, gateway/service-mesh identity, private platform channels, or combinations of controls.

## Configuration

Prefer platform/framework-native TLS and trust-store configuration. If the application owns certificates or key-store passwords, resolve sensitive values through the approved secret mechanism. A `SecretProvider` abstraction is optional and should be introduced only when it creates a useful boundary.

## Observability

Expose safe evidence for transport failures—handshake errors, certificate expiry alerts where supported, dependency connection failures—without logging certificates' private material, credentials, tokens, or sensitive payloads.

## LLM Instructions

- Inspect the target deployment boundary before generating application-level TLS configuration.
- Do not invent TLS versions, cipher suites, certificate lifetimes, mTLS, or a certificate authority when policy is absent.
- Prefer the target platform's supported secure defaults and current security baseline.
- Mark unresolved policy choices for security/platform review.

## Review Checklist

- [ ] Required network flows and trust boundaries are identified.
- [ ] Protection is enforced at the intended boundary for each applicable flow.
- [ ] Identity/certificate verification follows the approved trust model.
- [ ] Key/certificate secrets are not committed or logged.
- [ ] Renewal/rotation ownership is defined where certificates are managed by the project.
- [ ] Deployment evidence confirms the intended protection rather than relying only on code inspection.
