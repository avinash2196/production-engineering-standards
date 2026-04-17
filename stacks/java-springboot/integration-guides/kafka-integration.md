# Kafka Integration (Java Spring Boot)

## Purpose

Step-by-step guide for wiring Apache Kafka into a Spring Boot service through the `MessagePublisher` and `MessageSubscriber` capability interfaces, including producer/consumer configuration, serialization, error handling, observability, and fallback setup.

## Dependencies

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
</dependency>
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-core</artifactId>
</dependency>
```

## Producer Configuration

```yaml
# application.yml
spring:
  kafka:
    bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS:localhost:9092}
    producer:
      acks: all                    # wait for all replicas
      retries: 3
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
      properties:
        enable.idempotence: true   # exactly-once semantics at broker
        max.in.flight.requests.per.connection: 5
        delivery.timeout.ms: 30000
        linger.ms: 5              # micro-batch for throughput
```

## MessagePublisher Implementation

```java
@Component
@Profile("!fallback-kafka")
public class KafkaMessagePublisher implements MessagePublisher {
    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final MeterRegistry meterRegistry;
    private final Tracer tracer;

    @Override
    public void publish(String topic, Message message, PublishOptions options) {
        Span span = tracer.nextSpan().name("kafka-publish").tag("topic", topic).start();
        try (Tracer.SpanInScope ws = tracer.withSpan(span)) {
            ProducerRecord<String, Object> record = new ProducerRecord<>(topic, 
                options.getPartitionKey(), message.getBody());
            record.headers()
                .add("idempotencyKey", message.getIdempotencyKey().getBytes())
                .add("traceId", span.context().traceId().getBytes())
                .add("correlationId", message.getCorrelationId().getBytes());

            kafkaTemplate.send(record).whenComplete((result, ex) -> {
                if (ex != null) {
                    meterRegistry.counter("publisher_errors_total", "topic", topic).increment();
                    span.error(ex);
                    throw new PublishFailedException(topic, message.getIdempotencyKey(), ex);
                }
                meterRegistry.counter("publisher_messages_sent_total", "topic", topic).increment();
            });
        } finally {
            span.end();
        }
    }
}
```

## Consumer Configuration

```yaml
spring:
  kafka:
    consumer:
      group-id: ${spring.application.name}
      auto-offset-reset: earliest
      enable-auto-commit: false    # manual commit for at-least-once
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
      properties:
        max.poll.records: 100
        max.poll.interval.ms: 300000
```

## MessageSubscriber Implementation

```java
@Component
@Profile("!fallback-kafka")
public class KafkaMessageSubscriber implements MessageSubscriber {

    @KafkaListener(topics = "${app.topic.orders}", groupId = "${spring.application.name}")
    public void handleOrderEvents(ConsumerRecord<String, OrderEvent> record, Acknowledgment ack) {
        String idempotencyKey = new String(record.headers().lastHeader("idempotencyKey").value());
        String traceId = new String(record.headers().lastHeader("traceId").value());

        // Deduplication check
        if (dedupStore.exists(idempotencyKey)) {
            log.debug("Duplicate message, skipping: key={}", idempotencyKey);
            ack.acknowledge();
            return;
        }

        try {
            Span span = tracer.nextSpan().name("kafka-consume").tag("topic", record.topic()).start();
            try (Tracer.SpanInScope ws = tracer.withSpan(span)) {
                orderService.processEvent(record.value());
                dedupStore.mark(idempotencyKey, Duration.ofHours(24));
                ack.acknowledge();
                meterRegistry.counter("subscriber_messages_processed_total").increment();
            } finally {
                span.end();
            }
        } catch (Exception e) {
            log.error("Failed to process message: key={}, traceId={}", idempotencyKey, traceId, e);
            meterRegistry.counter("subscriber_errors_total").increment();
            // nack — message will be redelivered by Kafka
        }
    }
}
```

## Dead-Letter Topic

```java
@Bean
public ConcurrentKafkaListenerContainerFactory<String, Object> kafkaListenerContainerFactory(
        ConsumerFactory<String, Object> consumerFactory,
        KafkaTemplate<String, Object> kafkaTemplate) {
    var factory = new ConcurrentKafkaListenerContainerFactory<String, Object>();
    factory.setConsumerFactory(consumerFactory);
    factory.getContainerProperties().setAckMode(ContainerProperties.AckMode.MANUAL);
    factory.setCommonErrorHandler(new DefaultErrorHandler(
        new DeadLetterPublishingRecoverer(kafkaTemplate),
        new FixedBackOff(1000L, 3L)  // 3 retries, 1s between
    ));
    return factory;
}
```

## Fallback Wiring

```java
@Component
@Profile("fallback-kafka")
public class InMemoryMessagePublisher implements MessagePublisher {
    // See core/fallbacks/kafka-fallback.md for implementation
}
```

Activate in local dev via:
```yaml
# docker-compose.yml or .env.local
FALLBACK_KAFKA: "true"
```

## Observability

| Metric | Description |
|--------|-------------|
| `publisher_messages_sent_total` | Messages successfully published, by topic |
| `publisher_errors_total` | Publish failures, by topic |
| `subscriber_messages_processed_total` | Messages consumed and processed |
| `subscriber_errors_total` | Consumer processing failures |
| `subscriber_lag` | Consumer group lag (via JMX / Kafka metrics) |

Spring Boot auto-configures Kafka JMX metrics via Micrometer when `spring-kafka` is on the classpath.

## Testing

```java
@SpringBootTest
@EmbeddedKafka(topics = "test-orders", partitions = 1)
class KafkaIntegrationTest {
    @Autowired KafkaTemplate<String, Object> template;
    @Autowired OrderService orderService;

    @Test
    void should_process_order_event_from_kafka() {
        template.send("test-orders", new OrderEvent("order-123", "CREATED"));
        // assert orderService processed the event
    }
}
```

## References

- [MessagePublisher.md](../../../core/contracts/MessagePublisher.md)
- [MessageSubscriber.md](../../../core/contracts/MessageSubscriber.md)
- [kafka-fallback.md](../../../core/fallbacks/kafka-fallback.md)
- [messaging-abstraction standard](../../../standards/messaging-abstraction.md)
