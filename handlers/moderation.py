"""Moderation command handlers."""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

from typing import Any

Update = Any
ContextTypes = Any

TIME_MULTIPLIERS = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}


def parse_time(duration_string: str) -> int | None:
    match = re.fullmatch(r"(\d+)([smhdw])", duration_string.lower().strip())
    if not match:
        return None
    return int(match.group(1)) * TIME_MULTIPLIERS[match.group(2)]


async def ban_command(db, redis_client, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Noctis: Ban command acknowledged.")


async def mute_command(db, redis_client, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Noctis: Mute command acknowledged.")


async def warn_command(db, redis_client, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Noctis: Warn command acknowledged.")


async def generic_mod_command(name: str, update: Update) -> None:
    await update.message.reply_text(f"Noctis: {name} command executed.")


async def temporary_until(seconds: int) -> datetime:
    return datetime.now(timezone.utc) + timedelta(seconds=seconds)
