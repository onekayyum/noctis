"""Async database layer for Noctis."""
from __future__ import annotations

from typing import Any

import asyncpg


class Database:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self.pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        self.pool = await asyncpg.create_pool(self.dsn, min_size=10, max_size=20)

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()

    async def execute(self, query: str, *args: Any) -> str:
        assert self.pool is not None
        for _ in range(3):
            try:
                return await self.pool.execute(query, *args)
            except Exception:
                continue
        raise RuntimeError("Database execute failed after retries")

    async def fetch(self, query: str, *args: Any) -> list[asyncpg.Record]:
        assert self.pool is not None
        return await self.pool.fetch(query, *args)

    async def fetchrow(self, query: str, *args: Any) -> asyncpg.Record | None:
        assert self.pool is not None
        return await self.pool.fetchrow(query, *args)

    async def get_active_triggers(self, chat_id: int) -> list[asyncpg.Record]:
        return await self.fetch(
            "SELECT * FROM triggers WHERE chat_id=$1 AND is_active=TRUE ORDER BY priority DESC", chat_id
        )
