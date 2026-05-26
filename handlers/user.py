"""User-facing command handlers."""
from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Noctis stats: level 1, rep 0, messages 0, warnings 0")


async def generic_user_command(name: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Noctis {name} command executed")
