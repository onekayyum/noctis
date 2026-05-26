"""CAS integration using api.cas.chat export list."""
from __future__ import annotations

import asyncio
import csv
import io
import logging

import httpx

from redis_client import RedisClient

logger = logging.getLogger(__name__)


class CASClient:
    def __init__(self, redis_client: RedisClient, api_url: str, refresh_interval: int = 3600) -> None:
        self.redis_client = redis_client
        self.api_url = api_url
        self.refresh_interval = refresh_interval

    async def refresh(self) -> int:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(self.api_url)
                resp.raise_for_status()
            rows = csv.DictReader(io.StringIO(resp.text))
            ids = [row["user_id"].strip() for row in rows if row.get("user_id")]
            pipe = self.redis_client.redis.pipeline()
            pipe.delete("cas:spammers")
            if ids:
                pipe.sadd("cas:spammers", *ids)
            await pipe.execute()
            await self.redis_client.redis.set("cas:last_refresh_status", "ok")
            return len(ids)
        except Exception as exc:
            logger.exception("CAS refresh failed: %s", exc)
            await self.redis_client.redis.set("cas:last_refresh_status", "error")
            return 0

    async def initialize_cas_cache(self) -> None:
        await self.refresh()

    async def refresh_loop(self) -> None:
        while True:
            await asyncio.sleep(self.refresh_interval)
            await self.refresh()

    async def check_cas_spammer(self, user_id: int) -> bool:
        return await self.redis_client.is_cas_spammer(user_id)
