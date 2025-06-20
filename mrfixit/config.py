from dataclasses import dataclass, field

from mrfixit.adapters.database.config import DatabaseConfig, RedisConfig
from mrfixit.application.config import (
    AppConfig,
)
from mrfixit.presenters.bot.config import TgConfig


@dataclass(frozen=True, kw_only=True, slots=True)
class MainConfig:
    db: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())
    redis: RedisConfig = field(default_factory=lambda: RedisConfig())
    app: AppConfig = field(default_factory=lambda: AppConfig())
    bot: TgConfig = field(default_factory=lambda: TgConfig())
