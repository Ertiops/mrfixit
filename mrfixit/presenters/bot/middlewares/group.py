import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

log = logging.getLogger(__name__)


class GroupFilterMiddleware(BaseMiddleware):
    def __init__(self, allowed_chat_id: int) -> None:
        self.allowed_chat_id = allowed_chat_id

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        message = event.message or (
            event.callback_query.message if event.callback_query else None
        )
        if not message:
            return await handler(event, data)

        chat_id = message.chat.id
        log.info("GroupFilterMiddleware: chat_id=%s", chat_id)
        log.info("GroupFilterMiddleware: allowed_chat_id=%s", self.allowed_chat_id)
        if chat_id != self.allowed_chat_id:
            if event.message:
                await event.message.answer(
                    "⚠️ Бот работает только в утверждённой группе."
                )
            elif event.callback_query:
                await event.callback_query.answer(
                    "⚠️ Бот работает только в утверждённой группе.",
                    show_alert=True,
                )
            return

        return await handler(event, data)
