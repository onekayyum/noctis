"""Redis helpers for cache, rate limits, and sessions."""
from __future__ import annotations

from redis.asyncio import Redis


class RedisClient:
    def __init__(self, url: str) -> None:
        self.redis = Redis.from_url(url, decode_responses=True)

    async def close(self) -> None:
        await self.redis.close()

    async def is_cas_spammer(self, user_id: int) -> bool:
        return bool(await self.redis.sismember("cas:spammers", str(user_id)))

    async def add_pending_verification(self, chat_id: int, user_id: int) -> None:
        await self.redis.setex(f"verify:{chat_id}:{user_id}", 43200, "pending")

    async def rate_limit_ok(self, user_id: int, limit: int = 30) -> bool:
        key = f"ratelimit:{user_id}"
        count = await self.redis.incr(key)
        if count == 1:
            await self.redis.expire(key, 60)
        return count <= limit
