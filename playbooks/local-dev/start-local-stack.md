# Start Local Stack

Instructions to start local infrastructure using `docker-compose.dev.yml` for development with real service dependencies.

## Overview

While [run-with-fallbacks.md](run-with-fallbacks.md) lets you develop with zero infrastructure, sometimes you need real Kafka, Redis, PostgreSQL, or S3-compatible storage for integration testing or feature development. This guide covers spinning up a minimal local stack via Docker Compose.

## Prerequisites

- Docker Desktop (or Docker Engine + Compose plugin) installed.
- At least **4 GB RAM** allocated to Docker.
- Ports 5432, 6379, 9092, 9000 available.

## docker-compose.dev.yml

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app_db
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: local-dev-password
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app_user -d app_db"]
      interval: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      retries: 5

  kafka:
    image: confluentinc/cp-kafka:7.6.0
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@localhost:9093
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      CLUSTER_ID: local-dev-cluster-id-001
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    ports:
      - "9092:9092"
    healthcheck:
      test: kafka-topics --bootstrap-server localhost:9092 --list
      interval: 10s
      retries: 10

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports:
      - "9000:9000"    # S3 API
      - "9001:9001"    # Console
    volumes:
      - miniodata:/data

volumes:
  pgdata:
  miniodata:
```

## Usage

### Start Everything

```bash
docker compose -f docker-compose.dev.yml up -d
```

### Start Specific Services

```bash
# Only need PostgreSQL and Redis
docker compose -f docker-compose.dev.yml up -d postgres redis
```

### Check Health

```bash
docker compose -f docker-compose.dev.yml ps
```

All services should show `healthy` or `running`.

### Stop

```bash
docker compose -f docker-compose.dev.yml down

# Stop and remove volumes (clean reset)
docker compose -f docker-compose.dev.yml down -v
```

## Service Connection Config

With the local stack running, configure your service:

### Java (application-local.yml)

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/app_db
    username: app_user
    password: local-dev-password
  data:
    redis:
      host: localhost
      port: 6379
      ssl:
        enabled: false
  kafka:
    bootstrap-servers: localhost:9092

storage:
  provider: s3
  endpoint: http://localhost:9000
  bucket: dev-bucket
  region: us-east-1
```

### Python (.env.local)

```env
DATABASE_URL=postgresql://app_user:local-dev-password@localhost:5432/app_db
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_SSL=false
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
STORAGE_ENDPOINT_URL=http://localhost:9000
STORAGE_BUCKET=dev-bucket
```

## Creating the MinIO Bucket

```bash
# Install mc (MinIO client) or use the web console at http://localhost:9001
mc alias set local http://localhost:9000 minioadmin minioadmin
mc mb local/dev-bucket
```

## Hybrid Mode

You can mix real infra and fallbacks:

```bash
# Real Kafka + Redis, fallback storage
docker compose -f docker-compose.dev.yml up -d kafka redis
FALLBACK_STORAGE=local FALLBACK_SECRETS=env ./mvnw spring-boot:run -Dspring-boot.run.profiles=local
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port already in use | `docker compose down` or change port mapping |
| Kafka not starting | Ensure `CLUSTER_ID` is set (KRaft mode) |
| MinIO access denied | Verify `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` match your config |
| PostgreSQL connection refused | Wait for healthcheck to pass before starting app |

## References

- [Run with fallbacks](run-with-fallbacks.md)
- [Config model](../../standards/config/config-model.md)
- [Fallback strategy](../../standards/fallback-strategy.md)
