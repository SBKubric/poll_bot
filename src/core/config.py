import logging
import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class ModelConfig:
    allow_population_by_field_name = True


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    project_name: str = 'Polling Bot'

    # Настройки Redis
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cache_expiration_in_seconds: int = 300

    api_id: SecretStr = SecretStr("SECRET")
    api_hash: SecretStr = SecretStr("SECRET")
    bot_token: SecretStr = SecretStr("SECRET")

    # Корень проекта
    base_dir: str = os.path.dirname(os.path.dirname(__file__))

    log_level: str = "WARNING"

    sentry_dsn_auth: SecretStr = SecretStr("")

    db_url: str = "sqlite+aiosqlite:///poll_bot.db"
    sqlite_db: str = "poll_bot.db"


settings = Settings()  # type: ignore

if settings.sentry_dsn_auth:
    import sentry_sdk  # type: ignore

    sentry_sdk.init(
        dsn=settings.sentry_dsn_auth.get_secret_value(), traces_sample_rate=1.0
    )


# Применяем настройки логирования
logging.basicConfig(level=settings.log_level)
