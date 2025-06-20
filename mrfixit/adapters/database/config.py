from dataclasses import dataclass, field
from os import environ


@dataclass(frozen=True, kw_only=True, slots=True)
class DatabaseConfig:
    dsn: str = field(default_factory=lambda: environ["APP_DB_DSN"])
    pool_size: int = field(
        default_factory=lambda: int(environ.get("APP_DB_POOL_SIZE", 10))
    )
    pool_timeout: int = field(
        default_factory=lambda: int(environ.get("APP_DB_POOL_TIMEOUT", 10))
    )
    debug: bool = field(default_factory=lambda: bool(environ.get("APP_DB_DEBUG", True)))


@dataclass(frozen=True, slots=True, kw_only=True)
class RedisConfig:
    dsn: str = field(default_factory=lambda: environ["APP_REDIS_DSN"])
