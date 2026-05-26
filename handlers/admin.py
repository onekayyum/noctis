"""Administrative command handlers."""
from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes


async def cfg_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Noctis control panel: https://noctis.local/dashboard")


async def link_command(name: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Noctis {name}: https://noctis.local/{name}")
