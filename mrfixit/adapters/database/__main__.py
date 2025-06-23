import argparse
import logging
from dataclasses import dataclass, field
from os import environ

from alembic.config import CommandLine

from mrfixit.adapters.database.utils import make_alembic_config


@dataclass(frozen=True, kw_only=True, slots=True)
class DatabaseConfig:
    user: str = field(default_factory=lambda: environ.get("APP_DB_USER", "mrfixit"))
    password: str = field(
        default_factory=lambda: environ.get("APP_DB_PASSWORD", "mrfixit")
    )
    name: str = field(default_factory=lambda: environ.get("APP_DB_NAME", "mrfixit"))
    host: str = field(default_factory=lambda: environ.get("APP_DB_HOST", "127.0.0.1"))
    port: int = field(default_factory=lambda: int(environ.get("APP_DB_PORT", 5432)))

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
    options = alembic.parser.parse_args()
    db_config = DatabaseConfig()
    if "cmd" not in options:
        alembic.parser.error("Too few arguments")
        exit(128)
    else:
        config = make_alembic_config(options, pg_url=db_config.dsn)
        alembic.run_cmd(config, options)
        exit()


if __name__ == "__main__":
    main()
