from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from mrfixit.domains.entities.tech_request import (
    CreateTechRequest,
    TechRequestBuilding,
    TechRequestCategory,
    TechRequestStatus,
    UpdateTechRequest,
)
from mrfixit.domains.services.tech_request import TechRequestService
from mrfixit.domains.uow import AbstractUow
from mrfixit.presenters.bot.content.messages import tech_request as tech_request_msg
from mrfixit.presenters.bot.dialogs.states import (
    CreateTechRequestState,
    TechRequestListState,
)
from mrfixit.presenters.bot.utils.message_remover import delete_later


async def on_title_input(
    message: Message, widget: MessageInput, manager: DialogManager
) -> None:
    if not message.text:
        return
    manager.dialog_data["title"] = message.text.strip()
    await message.delete()
    await manager.switch_to(
        state=CreateTechRequestState.description,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def on_description_input(
    message: Message,
    widget: MessageInput,
    manager: DialogManager,
) -> None:
    if not message.text:
        return
    manager.dialog_data["description"] = message.text.strip()
    await message.delete()
    await manager.switch_to(
        state=CreateTechRequestState.photo,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def on_photo_input(
    message: Message, widget: MessageInput, manager: DialogManager
) -> None:
    if not message.photo:
        warning = await message.answer("❗️Пожалуйста, отправьте фотографию.")
        delete_later(warning)
        await manager.show(show_mode=ShowMode.DELETE_AND_SEND)
        return

    manager.dialog_data["file_id"] = message.photo[-1].file_id
    await message.delete()
    await manager.switch_to(
        state=CreateTechRequestState.confirm,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def on_create_tech_request(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    container = manager.middleware_data["dishka_container"]
    service: TechRequestService = await container.get(TechRequestService)
    uow: AbstractUow = await container.get(AbstractUow)
    async with uow:
        await service.create(
            input_dto=CreateTechRequest(
                title=manager.dialog_data["title"],
                description=manager.dialog_data["description"],
                category=TechRequestCategory(manager.dialog_data["category"]),
                status=TechRequestStatus.CREATED,
                building=TechRequestBuilding(manager.dialog_data["building"]),
                file_id=manager.dialog_data["file_id"],
            )
        )
    result_msg = await callback.message.answer(tech_request_msg.CREATED)  # type: ignore[union-attr]
    delete_later(result_msg)
    await manager.start(
        state=TechRequestListState.view,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def on_cancel_create_tech_request(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    result_msg = await callback.message.answer(tech_request_msg.NOT_CREATED)  # type: ignore[union-attr]
    delete_later(result_msg)
    await manager.start(
        state=TechRequestListState.view,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def on_cancel_view_clicked(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(
        state=TechRequestListState.view,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def on_mark_as_done_clicked(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    request_id = manager.dialog_data.get("request_id") or manager.start_data.get(  # type: ignore[union-attr]
        "request_id"
    )
    if not request_id:
        return
    container = manager.middleware_data["dishka_container"]
    service: TechRequestService = await container.get(TechRequestService)
    uow: AbstractUow = await container.get(AbstractUow)

    async with uow:
        await service.update_by_id(
            input_dto=UpdateTechRequest(id=request_id, status=TechRequestStatus.DONE)
        )
    await manager.start(
        state=TechRequestListState.view,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
