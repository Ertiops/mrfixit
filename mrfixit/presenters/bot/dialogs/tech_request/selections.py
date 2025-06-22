from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button, Select

from mrfixit.domains.entities.tech_request import (
    TechRequestBuilding,
    TechRequestCategory,
)
from mrfixit.presenters.bot.content.buttons import tech_request as tech_request_btn
from mrfixit.presenters.bot.dialogs.states import (
    CreateTechRequestState,
    GetTechRequestState,
)

CATEGORY_ITEMS: dict[TechRequestCategory, str] = {
    TechRequestCategory.URGENT: "Срочная",
    TechRequestCategory.ORDINARY: "Обычная",
}

BUILDING_ITEMS: dict[TechRequestBuilding, str] = {
    TechRequestBuilding.FOUNTAIN: tech_request_btn.FOUNTAIN,
    TechRequestBuilding.FORT_DIALOG: tech_request_btn.FORT_DIALOG,
}


async def on_building_selected(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager,
    item_id: str,
    **kwargs: Any,
) -> None:
    manager.dialog_data["building"] = item_id
    await manager.switch_to(
        state=CreateTechRequestState.category,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def on_category_selected(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
    item_id: str,
    **kwargs: Any,
) -> None:
    manager.dialog_data["category"] = item_id
    await manager.switch_to(
        state=CreateTechRequestState.title,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def on_tech_request_clicked(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id: str,
) -> None:
    manager.dialog_data["request_id"] = item_id
    await manager.start(
        state=GetTechRequestState.view,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
        data={"request_id": item_id},
    )
