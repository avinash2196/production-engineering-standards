# Observability (Java Spring Boot)

## Purpose

Comprehensive guide for instrumenting Spring Boot services with metrics, distributed tracing, structured logging, and health checks using Micrometer, OpenTelemetry, and Spring Boot Actuator.

## Dependencies

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-otel</artifactId>
</dependency>
<dependency>
    <groupId>io.opentelemetry</groupId>
    <artifactId>opentelemetry-exporter-otlp</artifactId>
</dependency>
```

---

## 1. Metrics (Micrometer + Prometheus)

### Configuration

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus,metrics
  metrics:
    tags:
      application: ${spring.application.name}
      environment: ${APP_ENV:local}
    distribution:
      percentiles-histogram:
        http.server.requests: true
      slo:
        http.server.requests: 50ms, 100ms, 250ms, 500ms, 1000ms
  prometheus:
    metrics:
      export:
        enabled: true
```

### Custom Business Metrics

```java
@Component
public class OrderMetrics {
    private final Counter ordersCreated;
    private final Timer orderProcessingTime;
    private final AtomicInteger activeOrders;

    public OrderMetrics(MeterRegistry registry) {
        this.ordersCreated = Counter.builder("orders_created_total")
            .description("Total orders created")
            .tag("service", "order-svc")
            .register(registry);
        this.orderProcessingTime = Timer.builder("order_processing_duration_seconds")
            .description("Time to process an order")
            .publishPercentileHistogram()
            .register(registry);
        this.activeOrders = registry.gauge("orders_active", new AtomicInteger(0));
    }

    public void recordOrderCreated() { ordersCreated.increment(); }
    public Timer.Sample startProcessing() { return Timer.start(); }
    public void stopProcessing(Timer.Sample sample) { sample.stop(orderProcessingTime); }
}
```

### Required Metrics per Service

Every service must expose:

| Metric | Type | Description |
|--------|------|-------------|
| `http_server_requests_seconds` | Histogram | Request latency (auto by Actuator) |
| `jvm_memory_used_bytes` | Gauge | JVM heap/non-heap (auto) |
| `jvm_gc_pause_seconds` | Timer | GC pause duration (auto) |
| `db_pool_active_connections` | Gauge | HikariCP active (auto) |
| `{domain}_operations_total` | Counter | Business operation counts |
| `{domain}_errors_total` | Counter | Business error counts |

---

## 2. Distributed Tracing (OpenTelemetry)

### Configuration

```yaml
management:
  tracing:
    sampling:
      probability: ${TRACE_SAMPLING_RATE:0.1}  # 10% in prod, 1.0 in dev
    propagation:
      type: w3c                                 # W3C TraceContext

# OTEL exporter
otel:
  exporter:
    otlp:
      endpoint: ${OTEL_EXPORTER_OTLP_ENDPOINT:http://localhost:4317}
      protocol: grpc
  resource:
    attributes:
      service.name: ${spring.application.name}
      deployment.environment: ${APP_ENV:local}
```

### Span Conventions

```java
@Service
public class OrderService {
    private final Tracer tracer;

    public Order createOrder(CreateOrderRequest request) {
        Span span = tracer.nextSpan()
            .name("OrderService.createOrder")
            .tag("order.type", request.getType())
            .start();
        try (Tracer.SpanInScope ws = tracer.withSpan(span)) {
            // business logic — downstream calls auto-propagate context
            Order order = processOrder(request);
            span.tag("order.id", order.getId());
            return order;
        } catch (Exception e) {
            span.error(e);
            throw e;
        } finally {
            span.end();
        }
    }
}
```

### Context Propagation

Spring Boot auto-propagates `traceparent` / `tracestate` headers for:
- `RestTemplate` / `WebClient` (via `ObservationRestTemplateCustomizer`)
- Kafka (`spring-kafka` auto-instruments headers)
- JDBC (via Micrometer JDBC instrumentation)

For custom propagation:
```java
// Inject trace context into outgoing headers manually
Span current = tracer.currentSpan();
headers.put("traceparent", current.context().traceId());
```

---

## 3. Structured Logging

### Configuration

```yaml
logging:
  pattern:
    console: >
      {"timestamp":"%d{ISO8601}","level":"%level","service":"${spring.application.name}",
       "traceId":"%X{traceId:-}","spanId":"%X{spanId:-}","thread":"%thread",
       "logger":"%logger{36}","message":"%msg"}%n
  level:
    root: INFO
    com.myorg: ${LOG_LEVEL:INFO}
    org.springframework.web: WARN
    org.hibernate.SQL: ${SQL_LOG_LEVEL:WARN}
```

### Logging Standards

```java
// DO: structured key-value context
log.info("Order created: orderId={}, userId={}, totalAmount={}", 
    order.getId(), order.getUserId(), order.getTotalAmount());

// DO: error with exception
log.error("Payment processing failed: orderId={}, provider={}", 
    orderId, paymentProvider, exception);

// DON'T: unstructured free text
log.info("Created order " + order.getId() + " for user " + userId);

// DON'T: log sensitive data
log.info("User authenticated: email={}, password={}", email, password); // NEVER
```

### MDC for Request Context

```java
@Component
public class RequestContextFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) 
            throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) req;
        try {
            MDC.put("requestId", request.getHeader("X-Request-Id"));
            MDC.put("userId", extractUserId(request));
            chain.doFilter(req, res);
        } finally {
            MDC.clear();
        }
    }
}
```

---

## 4. Health Checks

### Configuration

```yaml
management:
  endpoint:
    health:
      show-details: when-authorized
      group:
        readiness:
          include: db,redis,kafka
        liveness:
          include: livenessState
  health:
    redis:
      enabled: true
    kafka:
      enabled: true
```

### Custom Health Indicator

```java
@Component
public class ExternalApiHealthIndicator implements HealthIndicator {
    private final WebClient webClient;

    @Override
    public Health health() {
        try {
            webClient.get().uri("/health").retrieve()
                .toBodilessEntity().block(Duration.ofSeconds(2));
            return Health.up().withDetail("externalApi", "reachable").build();
        } catch (Exception e) {
            return Health.down().withDetail("externalApi", e.getMessage()).build();
        }
    }
}
```

### Kubernetes Probes

```yaml
# k8s deployment
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
```

---

## 5. Alerting Rules

Define in your monitoring platform (Prometheus/Grafana):

```yaml
# prometheus-rules.yml
groups:
  - name: spring-boot-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_server_requests_seconds_count{status=~"5.."}[5m]) / rate(http_server_requests_seconds_count[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
      - alert: HighLatencyP99
        expr: histogram_quantile(0.99, rate(http_server_requests_seconds_bucket[5m])) > 1.0
        for: 5m
        labels:
          severity: warning
      - alert: JvmMemoryHigh
        expr: jvm_memory_used_bytes{area="heap"} / jvm_memory_max_bytes{area="heap"} > 0.85
        for: 10m
        labels:
          severity: warning
```

## References

- [observability standard](../../standards/observability.md)
- [Spring Boot Actuator docs](https://docs.spring.io/spring-boot/reference/actuator/)
- [Micrometer docs](https://micrometer.io/docs)
