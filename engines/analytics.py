"""Analytics queries and aggregation."""
from __future__ import annotations

from database import Database


class AnalyticsEngine:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def top_level(self, chat_id: int, limit: int) -> list:
        return await self.db.fetch(
            "SELECT user_id, xp, level FROM members WHERE chat_id=$1 ORDER BY level DESC LIMIT $2", chat_id, limit
        )

    async def heatmap(self, chat_id: int) -> list:
        return await self.db.fetch(
            "SELECT hour_of_day, SUM(count) AS total FROM activity_log WHERE chat_id=$1 GROUP BY hour_of_day", chat_id
        )

    async def growth(self, chat_id: int) -> list:
        return await self.db.fetch(
            "SELECT DATE(joined_date) AS d, COUNT(*) FROM members WHERE chat_id=$1 GROUP BY DATE(joined_date)", chat_id
        )
