"""Database-backed local message publisher.

The adapter stores inspectable messages in a local database table. It preserves
restart durability but does not reproduce broker partitioning, consumer groups,
or global ordering. It must not be selected in production.
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

_TABLE_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


@dataclass(frozen=True)
class OutboxMessage:
    topic: str
    payload: Any
    message_key: str | None = None
    headers: dict[str, str] = field(default_factory=dict)
    status: str = "PENDING"
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class OutboxStore(Protocol):
    async def append(self, message: OutboxMessage) -> None: ...


class DatabaseOutboxMessagePublisher:
    def __init__(self, store: OutboxStore) -> None:
        self._store = store

    async def publish(
        self,
        topic: str,
        message: Any,
        key: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        await self._store.append(
            OutboxMessage(
                topic=topic,
                payload=message,
                message_key=key,
                headers=headers or {},
            )
        )


class SqlAlchemyOutboxStore:
    """Minimal PostgreSQL-compatible outbox store for local development."""

    def __init__(
        self,
        database_url: str,
        table_name: str = "outbox_message",
        engine: AsyncEngine | None = None,
    ) -> None:
        if not _TABLE_NAME.fullmatch(table_name):
            raise ValueError("Outbox table name must be a simple SQL identifier")
        self._table_name = table_name
        self._database_url = database_url
        self._engine = engine
        self._schema_ready = False

    def _get_engine(self) -> AsyncEngine:
        if self._engine is None:
            self._engine = create_async_engine(self._database_url)
        return self._engine

    async def append(self, message: OutboxMessage) -> None:
        async with self._get_engine().begin() as connection:
            if not self._schema_ready:
                await connection.execute(
                    text(
                        f"""
                        CREATE TABLE IF NOT EXISTS {self._table_name} (
                            message_id VARCHAR(36) PRIMARY KEY,
                            topic VARCHAR(255) NOT NULL,
                            message_key VARCHAR(255),
                            payload_json TEXT NOT NULL,
                            headers_json TEXT NOT NULL,
                            status VARCHAR(32) NOT NULL,
                            created_at TIMESTAMP WITH TIME ZONE NOT NULL
                        )
                        """
                    )
                )
                self._schema_ready = True
            await connection.execute(
                text(
                    f"""
                    INSERT INTO {self._table_name} (
                        message_id,
                        topic,
                        message_key,
                        payload_json,
                        headers_json,
                        status,
                        created_at
                    ) VALUES (
                        :message_id,
                        :topic,
                        :message_key,
                        :payload_json,
                        :headers_json,
                        :status,
                        :created_at
                    )
                    """
                ),
                {
                    "message_id": message.message_id,
                    "topic": message.topic,
                    "message_key": message.message_key,
                    "payload_json": json.dumps(message.payload),
                    "headers_json": json.dumps(message.headers),
                    "status": message.status,
                    "created_at": message.created_at,
                },
            )
