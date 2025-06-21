from collections import defaultdict
from typing import Any
from uuid import UUID

from aiogram.types import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from mrfixit.domains.entities.tech_request import (
    TechRequestBuilding,
    TechRequestCategory,
    TechRequestListParams,
    TechRequestStatus,
)
from mrfixit.domains.services.tech_request import TechRequestService
from mrfixit.domains.uow import AbstractUow
from mrfixit.presenters.bot.dialogs.tech_request.formatters import (
    format_tech_request_line,
)
from mrfixit.presenters.bot.dialogs.tech_request.selections import (
    BUILDING_ITEMS,
    CATEGORY_ITEMS,
)


async def get_tech_request_preview(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    data = dialog_manager.dialog_data
    return dict(
        building=BUILDING_ITEMS.get(data.get("building"), "❓"),  # type: ignore[arg-type]
        category=CATEGORY_ITEMS.get(data.get("category"), "❓"),  # type: ignore[arg-type]
        title=data.get("title", "❓"),
        description=data.get("description", "❓"),
        file_status="✅ Приложено" if data.get("file_id") else "❌ Не прикреплено",
    )


async def get_tech_request_list_context(
    dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    service: TechRequestService = await container.get(TechRequestService)
    uow: AbstractUow = await container.get(AbstractUow)

    async with uow:
        all_requests = await service.get_list(
            input_dto=TechRequestListParams(limit=100, offset=0)
        )

    grouped: dict[TechRequestBuilding, dict[str, list]] = defaultdict(
        lambda: {"urgent": [], "ordinary": [], "done": []}
    )
    text_lines: list[str] = []

    for req in all_requests.items:
        emoji = "🔴" if req.category == TechRequestCategory.URGENT else "🔵"
        item_dict = dict(id=str(req.id), title=req.title, emoji=emoji)

        if req.status == TechRequestStatus.DONE:
            grouped[req.building]["done"].append((req, item_dict))
        elif req.category == TechRequestCategory.URGENT:
            grouped[req.building]["urgent"].append((req, item_dict))
        else:
            grouped[req.building]["ordinary"].append((req, item_dict))

    for building in TechRequestBuilding:
        title = BUILDING_ITEMS[building]
        text_lines.append(f"<b>{title}</b>")

        for section in ("urgent", "ordinary", "done"):
            for req, _ in sorted(
                grouped[building][section], key=lambda pair: pair[0].created_at
            ):
                text_lines.append(format_tech_request_line(req))

    def serialize(building: TechRequestBuilding) -> list[dict]:
        return [
            item_dict
            for section in ("urgent", "ordinary")
            for _, item_dict in grouped[building][section]
        ]

    return dict(
        text="\n".join(text_lines),
        fountain_requests=serialize(TechRequestBuilding.FONTAN),
        fort_dialog_requests=serialize(TechRequestBuilding.FORT_DIALOG),
    )


async def get_single_tech_request(
    dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    service: TechRequestService = await container.get(TechRequestService)
    uow: AbstractUow = await container.get(AbstractUow)

    request_id = dialog_manager.start_data.get(  # type: ignore[union-attr]
        "request_id"
    ) or dialog_manager.dialog_data.get("request_id")

    async with uow:
        request = await service.get_by_id(input_id=UUID(request_id))

    return dict(
        title=request.title,
        description=request.description,
        category=CATEGORY_ITEMS[request.category],
        building=BUILDING_ITEMS[request.building],
        photo=MediaAttachment(
            type=ContentType.PHOTO,
            file_id=MediaId(request.file_id),
        ),
    )
