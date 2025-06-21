from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode

from mrfixit.presenters.bot.dialogs.states import (
    CreateTechRequestState,
    TechRequestListState,
)
from mrfixit.presenters.bot.utils.message_remover import delete_later


async def initiate_get_tech_requests(
    message: Message, dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        state=TechRequestListState.view,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
    delete_later(message)


async def initiate_create_tech_request(
    message: Message, dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        state=CreateTechRequestState.building,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
    delete_later(message)
