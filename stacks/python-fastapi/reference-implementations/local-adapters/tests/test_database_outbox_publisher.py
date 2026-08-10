"""Unit tests for the database-backed local message publisher."""

from __future__ import annotations

import unittest
from typing import Any

from app.infrastructure.local.database_outbox_publisher import (
    DatabaseOutboxMessagePublisher,
    OutboxMessage,
)


class RecordingOutboxStore:
    def __init__(self) -> None:
        self.messages: list[OutboxMessage] = []

    async def append(self, message: OutboxMessage) -> None:
        self.messages.append(message)


class DatabaseOutboxMessagePublisherTest(unittest.IsolatedAsyncioTestCase):
    async def test_publish_writes_inspectable_outbox_message(self) -> None:
        store = RecordingOutboxStore()
        publisher = DatabaseOutboxMessagePublisher(store)
        payload: dict[str, Any] = {"quoteId": "Q-1", "amount": 125}

        await publisher.publish("quote.created", payload, key="Q-1")

        self.assertEqual(1, len(store.messages))
        message = store.messages[0]
        self.assertEqual("quote.created", message.topic)
        self.assertEqual("Q-1", message.message_key)
        self.assertEqual(payload, message.payload)
        self.assertEqual("PENDING", message.status)


if __name__ == "__main__":
    unittest.main()
