import logging
from collections.abc import Sequence

from aiogram import BaseMiddleware

from mrfixit.config import MainConfig
from mrfixit.presenters.bot.middlewares.group import GroupFilterMiddleware

log = logging.getLogger(__name__)

config = MainConfig()


bot_middlewares: Sequence[BaseMiddleware] = [
    GroupFilterMiddleware(allowed_chat_id=config.bot.allowed_chat_id),
]
