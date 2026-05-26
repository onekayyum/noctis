# Noctis (@Noctisrobot)

Production-oriented Telegram moderation bot and web panel.

## Setup
1. Copy `.env` and set BOT_TOKEN, DATABASE_URL, REDIS_URL.
2. Apply `schema.sql`.
3. Install deps: `pip install -r requirements.txt`.
4. Run bot: `python bot.py`.
5. Run web: `uvicorn web.main:app --reload`.

## Features
- Moderation commands (ban/mute/kick/warn/whitelist)
- CAS integration (`https://api.cas.chat/export.csv`) with hourly refresh
- Trigger engine with wildcard and regex support
- XP/levels and analytics query engine
- FastAPI admin endpoints with JWT auth
- Dockerized horizontal bot shards
