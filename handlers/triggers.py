"""Trigger management handlers."""
from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes


async def addtrigger_command(db, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Noctis trigger added")


async def listtriggers_command(db, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Noctis triggers listed")


async def removetrigger_command(db, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Noctis trigger removed")


async def edittrigger_command(db, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Noctis trigger edited")
