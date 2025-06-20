from dataclasses import dataclass, field
from os import environ


@dataclass(frozen=True, kw_only=True, slots=True)
class TgConfig:
    token: str = field(default_factory=lambda: environ.get("APP_TG_BOT_TOKEN", "token"))
    allowed_chat_id: int = field(
        default_factory=lambda: int(environ.get("APP_TG_ALLOWED_CHAT_ID", 0))
    )
