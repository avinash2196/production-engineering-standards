# Scalability

Purpose
- Define horizontal scaling patterns and capacity considerations for services and stateful dependencies.

Mandatory Rules
- Design stateless service instances where possible. Stateful components must be sharded or partitioned explicitly.
- Define and document scalability limits (throughput, connections) and provide autoscaling metrics.

Defaults
- Use instance-based horizontality: scale by adding instances behind a load balancer; prefer sticky-less designs.
- For stateful stores, partition by a business key and plan for re-sharding procedures.

Anti-patterns
- Relying on single-instance vertical scaling without documented limits.
- Storing global mutable state in-process without reconciliation.

LLM instructions
- When proposing scaling changes, include target CPU/RPS thresholds and suggest autoscaling policies.
- Ask the user if the system has regulatory constraints that limit multi-region scaling.

Review checklist
- [ ] Service is stateless or state is externally partitioned.
- [ ] Autoscaling metrics and thresholds documented.
- [ ] Re-sharding and migration procedures documented for stateful components.
