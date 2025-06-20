from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Select

from mrfixit.domains.entities.tech_request import (
    TechRequestBuilding,
    TechRequestCategory,
)
from mrfixit.presenters.bot.dialogs.states import (
    CreateTechRequestState,
    GetTechRequestState,
)

CATEGORY_ITEMS: dict[TechRequestCategory, str] = {
    TechRequestCategory.URGENT: "Срочная",
    TechRequestCategory.ORDINARY: "Обычная",
}

BUILDING_ITEMS: dict[TechRequestBuilding, str] = {
    TechRequestBuilding.FONTAN: "Фонтан",
    TechRequestBuilding.FORT_DIALOG: "Форт Диалог",
}


async def on_building_selected(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager,
    item_id: str,
    **kwargs: Any,
) -> None:
    manager.dialog_data["building"] = item_id
    await manager.switch_to(CreateTechRequestState.category)


async def on_category_selected(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
    item_id: str,
    **kwargs: Any,
) -> None:
    manager.dialog_data["category"] = item_id
    await manager.switch_to(CreateTechRequestState.title)


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
        data={"request_id": item_id},
    )
