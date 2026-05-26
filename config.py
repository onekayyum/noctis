"""Configuration for Noctis bot and web services."""
from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: str = Field(alias="BOT_TOKEN")
    database_url: str = Field(alias="DATABASE_URL")
    redis_url: str = Field(alias="REDIS_URL")
    cas_api_url: str = Field(default="https://api.cas.chat/export.csv", alias="CAS_API_URL")
    cas_refresh_hours: int = Field(default=1, alias="CAS_REFRESH_HOURS")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    jwt_secret: str = Field(default="change-me", alias="JWT_SECRET")
    owner_id: int = Field(default=0, alias="OWNER_ID")


settings = Settings()
