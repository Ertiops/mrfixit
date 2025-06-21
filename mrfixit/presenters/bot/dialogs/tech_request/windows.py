from aiogram.types import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Group, Row, Select
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from mrfixit.presenters.bot.dialogs.states import (
    CreateTechRequestState,
    GetTechRequestState,
    TechRequestListState,
)
from mrfixit.presenters.bot.dialogs.tech_request.getters import (
    get_single_tech_request,
    get_tech_request_list_context,
    get_tech_request_preview,
)
from mrfixit.presenters.bot.dialogs.tech_request.handlers import (
    on_cancel_create_tech_request,
    on_cancel_view_clicked,
    on_create_tech_request,
    on_description_input,
    on_mark_as_done_clicked,
    on_photo_input,
    on_title_input,
)
from mrfixit.presenters.bot.dialogs.tech_request.selections import (
    BUILDING_ITEMS,
    CATEGORY_ITEMS,
    on_building_selected,
    on_category_selected,
    on_tech_request_clicked,
)
from mrfixit.presenters.bot.dialogs.utils.handlers import on_unexpected_input


def building_selection_window() -> Window:
    return Window(
        Const("🏢 Выберите здание:"),
        MessageInput(on_unexpected_input, content_types=ContentType.ANY),
        Select(
            id="building_select",
            items=BUILDING_ITEMS.items(),  # type: ignore[arg-type]
            item_id_getter=lambda item: item[0],
            text=Format("{item[1]}"),
            on_click=on_building_selected,  # type: ignore[arg-type]
            type_factory=str,
        ),
        state=CreateTechRequestState.building,
    )


def category_selection_window() -> Window:
    return Window(
        Const("🏷 Выберите категорию:"),
        MessageInput(on_unexpected_input, content_types=ContentType.ANY),
        Select(
            id="category_select",
            items=CATEGORY_ITEMS.items(),  # type: ignore[arg-type]
            item_id_getter=lambda item: item[0],
            text=Format("{item[1]}"),
            on_click=on_category_selected,  # type: ignore[arg-type]
            type_factory=str,
        ),
        state=CreateTechRequestState.category,
    )


def title_input_window() -> Window:
    return Window(
        Const("✍️ Введите заголовок заявки:"),
        MessageInput(on_title_input, content_types=ContentType.TEXT),
        state=CreateTechRequestState.title,
    )


def description_input_window() -> Window:
    return Window(
        Const("📝 Введите описание проблемы:"),
        MessageInput(on_description_input, content_types=ContentType.TEXT),
        state=CreateTechRequestState.description,
    )


def photo_input_window() -> Window:
    return Window(
        Const("📸 Отправьте фотографию:"),
        MessageInput(on_photo_input, content_types=ContentType.ANY),
        state=CreateTechRequestState.photo,
    )


def request_preview_window() -> Window:
    return Window(
        MessageInput(on_unexpected_input, content_types=ContentType.ANY),
        Format(
            "🧾 Предпросмотр заявки:\n\n"
            "🏢 Здание: {building}\n"
            "🏷 Категория: {category}\n"
            "📌 Заголовок: {title}\n"
            "📝 Описание: {description}\n"
            "📎 Фото: {file_status}"
        ),
        Row(
            Button(Const("✅ Создать"), id="create", on_click=on_create_tech_request),
            Button(
                Const("❌ Отмена"), id="cancel", on_click=on_cancel_create_tech_request
            ),
        ),
        state=CreateTechRequestState.confirm,
        getter=get_tech_request_preview,
    )


def tech_request_list_window() -> Window:
    return Window(
        Format("{text}"),
        Button(Const("🏢 Фонтан"), id="fountain_title"),
        Group(
            Select(
                id="fountain_select",
                items="fountain_requests",
                item_id_getter=lambda item: item["id"],
                text=Format("{item[emoji]} {item[title]}"),
                on_click=on_tech_request_clicked,
            ),
            width=1,
            id="fountain_group",
        ),
        Button(Const("🏢 Форт Диалог"), id="fort_dialog_title"),
        Group(
            Select(
                id="fort_dialog_select",
                items="fort_dialog_requests",
                item_id_getter=lambda item: item["id"],
                text=Format("{item[emoji]} {item[title]}"),
                on_click=on_tech_request_clicked,
            ),
            width=1,
            id="fort_dialog_group",
        ),
        state=TechRequestListState.view,
        getter=get_tech_request_list_context,
    )


def tech_request_view_window() -> Window:
    return Window(
        MessageInput(on_unexpected_input, content_types=ContentType.ANY),
        DynamicMedia("photo"),
        Format(
            "<b>📝 Заявка</b>\n\n"
            "📌 <b>{title}</b>\n"
            "🏢 Здание: {building}\n"
            "🏷 Категория: {category}\n"
            "🗒 Описание:\n{description}"
        ),
        Button(
            Const("🔙 Назад"),
            id="back",
            on_click=on_cancel_view_clicked,
        ),
        Button(
            Const("✅ Выполнить"),
            id="mark_done",
            on_click=on_mark_as_done_clicked,
        ),
        state=GetTechRequestState.view,
        getter=get_single_tech_request,
    )
