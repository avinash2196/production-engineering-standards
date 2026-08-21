# ConfigProvider

## Purpose

Optional capability contract for projects that need an application-owned configuration boundary—for example because multiple sources, runtime refresh, portability, or testability justify it.

**Do not introduce `ConfigProvider` when framework/platform-native typed configuration is sufficient.** The canonical policy is [Configuration Management](../standards/configuration-management.md).

## Contract Shape

A project that adopts this capability may need operations such as:

- read an optional value;
- read a required value;
- bind/convert to an expected type;
- expose refresh/change behavior **only if runtime mutation is actually supported**.

The exact API belongs to the target language/framework and approved requirements. A minimal boundary may be smaller than the examples historically used by this repository.

## Source Model

`ConfigProvider` does not define a universal source list or precedence. If multiple sources are used:

- use framework/platform precedence where appropriate;
- otherwise document and test the chosen order;
- define which sources can mutate at runtime;
- define source-unavailable and invalid-value behavior;
- avoid silent fallback when it would change correctness/security behavior.

Do not assume operator → dynamic → environment → file → build defaults, a 30-second refresh, or centralized dynamic configuration.

## Secrets

Keep secret handling separate from ordinary non-sensitive configuration according to the project's approved security/platform model. If the project adopts the optional [`SecretProvider`](SecretProvider.md) boundary, use it for the secret values that boundary owns. Native secret injection/binding is also valid when that is the approved design.

Do not classify a value as a secret solely from a substring in its key; use the project data/security model while treating suspicious names as a review signal.

## Failure and Validation

- Validate required values early enough to fail clearly and safely.
- Do not expose sensitive values in validation errors or logs.
- Use defaults only when they are semantically safe and intentional.
- Runtime refresh/change listeners are optional and require explicit dynamic-config requirements.

## Example Boundary

```java
public interface ConfigProvider {
    Optional<String> get(String key);
    String getRequired(String key);
}
```

This is illustrative, not mandatory. Prefer typed framework configuration when it provides a clearer API.

## LLM Instructions

- First inspect whether the target project already has an established configuration mechanism.
- Do not create `ConfigProvider`, custom source classes, dynamic refresh, or precedence logic unless justified.
- If the project adopts this contract, keep its API no larger than the approved use cases require.
- Document source/precedence/failure decisions that materially affect runtime behavior.

## Review Checklist

- [ ] A custom configuration boundary is actually justified.
- [ ] Active sources and precedence come from the real stack/design.
- [ ] Required/default behavior is explicit and safe.
- [ ] Dynamic refresh exists only when required.
- [ ] Secret values follow the approved secret-management design.
