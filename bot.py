"""Main entrypoint for @Noctisrobot."""
from __future__ import annotations

import asyncio
import logging
from functools import partial

from telegram.ext import Application, CommandHandler

from cas_client import CASClient
from config import settings
from database import Database
from handlers import admin, moderation, triggers, user
from redis_client import RedisClient

logging.basicConfig(level=settings.log_level)


async def register_handlers(app: Application, db: Database, redis_client: RedisClient) -> None:
    app.add_handler(CommandHandler("ban", partial(moderation.ban_command, db, redis_client)))
    app.add_handler(CommandHandler("sban", partial(moderation.ban_command, db, redis_client)))
    app.add_handler(CommandHandler("unban", partial(moderation.ban_command, db, redis_client)))
    app.add_handler(CommandHandler("mute", partial(moderation.mute_command, db, redis_client)))
    app.add_handler(CommandHandler("smute", partial(moderation.mute_command, db, redis_client)))
    app.add_handler(CommandHandler("unmute", partial(moderation.mute_command, db, redis_client)))
    app.add_handler(CommandHandler("kick", partial(moderation.ban_command, db, redis_client)))
    app.add_handler(CommandHandler("skick", partial(moderation.ban_command, db, redis_client)))
    app.add_handler(CommandHandler("warn", partial(moderation.warn_command, db, redis_client)))
    app.add_handler(CommandHandler("unwarn", partial(moderation.warn_command, db, redis_client)))
    app.add_handler(CommandHandler("warnings", partial(moderation.warn_command, db, redis_client)))
    app.add_handler(CommandHandler("ro", partial(moderation.mute_command, db, redis_client)))
    app.add_handler(CommandHandler("whitelist", partial(moderation.ban_command, db, redis_client)))
    app.add_handler(CommandHandler("unwhitelist", partial(moderation.ban_command, db, redis_client)))
    app.add_handler(CommandHandler("reload", partial(moderation.ban_command, db, redis_client)))
    app.add_handler(CommandHandler("d", user.stats_command))
    app.add_handler(CommandHandler("pin", user.stats_command))
    app.add_handler(CommandHandler("unpin", user.stats_command))
    app.add_handler(CommandHandler("report", user.stats_command))
    app.add_handler(CommandHandler("check_rights", user.stats_command))
    app.add_handler(CommandHandler("rmkb", user.stats_command))
    app.add_handler(CommandHandler("stats", user.stats_command))
    app.add_handler(CommandHandler("toplvl", user.stats_command))
    app.add_handler(CommandHandler("toprep", user.stats_command))
    app.add_handler(CommandHandler("bottomrep", user.stats_command))
    app.add_handler(CommandHandler("id", user.stats_command))
    app.add_handler(CommandHandler("adminlist", user.stats_command))
    app.add_handler(CommandHandler("cfg", admin.cfg_command))
    for cmd in ["log", "mod", "settings", "export", "scan_cas"]:
        app.add_handler(CommandHandler(cmd, partial(admin.link_command, cmd)))
    app.add_handler(CommandHandler("addtrigger", partial(triggers.addtrigger_command, db)))
    app.add_handler(CommandHandler("listtriggers", partial(triggers.listtriggers_command, db)))
    app.add_handler(CommandHandler("removetrigger", partial(triggers.removetrigger_command, db)))
    app.add_handler(CommandHandler("edittrigger", partial(triggers.edittrigger_command, db)))


async def main() -> None:
    db = Database(settings.database_url)
    redis_client = RedisClient(settings.redis_url)
    await db.connect()

    cas_client = CASClient(redis_client, settings.cas_api_url, settings.cas_refresh_hours * 3600)
    await cas_client.initialize_cas_cache()
    asyncio.create_task(cas_client.refresh_loop())

    app = Application.builder().token(settings.bot_token).build()
    await register_handlers(app, db, redis_client)
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()


if __name__ == "__main__":
    asyncio.run(main())
