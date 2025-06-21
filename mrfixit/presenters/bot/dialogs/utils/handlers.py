from aiogram.types import Message
from aiogram_dialog.api.entities import ShowMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.input import MessageInput


async def on_unexpected_input(
    message: Message,
    widget: MessageInput,
    manager: DialogManager,
) -> None:
    await manager.show(show_mode=ShowMode.DELETE_AND_SEND)
