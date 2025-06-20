import asyncio

from aiogram.types import Message

from mrfixit.application.exceptions import MrFixitException


def delete_later(message: Message, delay: int = 5) -> None:
    async def _delete() -> None:
        await asyncio.sleep(delay)
        try:
            await message.delete()
        except MrFixitException:
            pass

    asyncio.create_task(_delete()).add_done_callback(lambda _: None)
