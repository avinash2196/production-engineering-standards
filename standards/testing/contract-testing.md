# Contract Testing

Consumer-driven contract testing guidance for verifying API compatibility between services.

## Purpose

Ensure that changes to a provider service do not break consumer expectations, without requiring full end-to-end test environments.

## Mandatory Rules

- Every service that exposes an API consumed by another team must have contract tests.
- Contracts are **consumer-driven**: the consumer defines expected interactions, the provider verifies them.
- Contract tests run in CI on every PR — breaking a contract blocks merge.
- Contracts are stored in a shared **Pact Broker** (or equivalent contract repository).

## Workflow

```
1. Consumer writes a contract test ("when I call GET /orders/123, I expect {...}")
2. Contract is published to the Pact Broker
3. Provider CI job pulls consumer contracts and verifies against its actual API
4. If verification fails → provider build fails
5. If verification passes → "can-i-deploy" check allows release
```

## Consumer Side (Java)

```java
@ExtendWith(PactConsumerTestExt.class)
@PactTestFor(providerName = "order-service")
class OrderClientContractTest {

    @Pact(provider = "order-service", consumer = "payment-service")
    V4Pact getOrderPact(PactDslWithProvider builder) {
        return builder
            .given("order abc-123 exists")
            .uponReceiving("a request for order abc-123")
            .path("/api/v1/orders/abc-123")
            .method("GET")
            .willRespondWith()
            .status(200)
            .body(newJsonBody(o -> {
                o.stringType("id", "abc-123");
                o.stringType("status", "CONFIRMED");
                o.decimalType("totalAmount", 99.99);
            }).build())
            .toPact(V4Pact.class);
    }

    @Test
    @PactTestFor(pactMethod = "getOrderPact")
    void should_parse_order_response(MockServer mockServer) {
        OrderClient client = new OrderClient(mockServer.getUrl());
        OrderResponse order = client.getOrder("abc-123");
        assertThat(order.getId()).isEqualTo("abc-123");
        assertThat(order.getStatus()).isEqualTo("CONFIRMED");
    }
}
```

## Consumer Side (Python)

```python
import pytest
from pact import Consumer, Provider

@pytest.fixture(scope="module")
def pact():
    p = Consumer("payment-service").has_pact_with(
        Provider("order-service"),
        pact_dir="./pacts",
    )
    p.start_service()
    yield p
    p.stop_service()
    p.verify()

def test_get_order(pact):
    expected = {"id": "abc-123", "status": "CONFIRMED", "totalAmount": 99.99}
    (pact
        .given("order abc-123 exists")
        .upon_receiving("a request for order abc-123")
        .with_request("GET", "/api/v1/orders/abc-123")
        .will_respond_with(200, body=expected))

    with pact:
        result = order_client.get_order("abc-123")
        assert result["id"] == "abc-123"
```

## Provider Verification

```java
// Provider side: run in CI
@Provider("order-service")
@PactBroker(url = "${PACT_BROKER_URL}")
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class OrderProviderContractTest {

    @TestTemplate
    @ExtendWith(PactVerificationInvocationContextProvider.class)
    void verifyPact(PactVerificationContext context) {
        context.verifyInteraction();
    }

    @State("order abc-123 exists")
    void setupOrder() {
        orderRepository.save(new Order("abc-123", OrderStatus.CONFIRMED, new BigDecimal("99.99")));
    }
}
```

## CI Integration

```yaml
# GitHub Actions example
jobs:
  consumer-contract:
    steps:
      - run: ./mvnw test -pl payment-service -Dtest="*ContractTest"
      - run: pact-broker publish ./pacts --consumer-app-version=${{ github.sha }}

  provider-verify:
    needs: consumer-contract
    steps:
      - run: ./mvnw test -pl order-service -Dtest="*ProviderContractTest"

  can-i-deploy:
    needs: provider-verify
    steps:
      - run: pact-broker can-i-deploy --pacticipant=order-service --version=${{ github.sha }} --to=production
```

## When to Use Contract Tests

| Scenario | Use contract test? |
|----------|-------------------|
| Service A calls Service B's REST API | **Yes** |
| Service A consumes Service B's Kafka events | **Yes** (message pact) |
| Frontend calls backend API | Yes (optional, Pact supports it) |
| Internal module calls within one service | No — use unit tests |
| Third-party API you don't control | No — use integration tests with WireMock |

## Defaults

- Tool: [Pact](https://docs.pact.io/) (JVM + Python supported).
- Broker: Self-hosted Pact Broker or PactFlow SaaS.
- Contracts published on every consumer PR.
- Provider verification triggered by broker webhook or CI schedule.

## Anti-Patterns

| Anti-Pattern | Why it's wrong |
|-------------|----------------|
| Provider writes the contracts | Defeats consumer-driven purpose — contracts reflect what consumers actually need |
| Exact-match on every field | Contracts should be loose (type-based matching) to allow additive changes |
| Skipping `can-i-deploy` check | Allows incompatible versions to reach production |
| Contract tests as integration tests | Contracts verify shape, not business logic |

## LLM Instructions

- When a user creates a new service-to-service call, suggest writing a Pact consumer test.
- Use type-based matchers (`stringType`, `decimalType`) rather than exact values.
- Generate both the consumer contract and the provider state setup.

## Review Checklist

- [ ] Consumer contracts exist for all cross-team API calls.
- [ ] Contracts use type-based matchers (not exact value matching).
- [ ] Provider verification is wired into CI.
- [ ] `can-i-deploy` gate is configured before production releases.
- [ ] Message contracts exist for event-driven integrations.

## References

- [testing-standards.md](../testing/) (parent)
- [Pact documentation](https://docs.pact.io/)
- [dto-guidelines.md](../dto-guidelines.md)
