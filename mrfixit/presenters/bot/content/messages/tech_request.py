from typing import Final

FILE_ATTACHED: Final = "✅ Приложено"
FILE_NOT_ATTACHED: Final = "❌ Не прикреплено"

CREATED: Final = "✅ Заявка успешно создана."
NOT_CREATED: Final = "❌ Создание заявки отменено."

TITLE_INPUT: Final = "✍️ Введите заголовок заявки:"
DESCRIPTION_INPUT: Final = "📝 Введите описание проблемы:"
PHOTO_INPUT: Final = "📸 Отправьте фотографию:"

CREATE_PREVIEW: Final = (
    "🧾 Предпросмотр заявки:\n\n"
    "🏢 Здание: {building}\n"
    "🏷 Категория: {category}\n"
    "📌 Заголовок: {title}\n"
    "📝 Описание: {description}\n"
    "📎 Фото: {file_status}"
)


UPDATE_PREVIEW: Final = (
    "<b>📝 Заявка</b>\n\n"
    "📌 <b>{title}</b>\n"
    "🏢 Здание: {building}\n"
    "🏷 Категория: {category}\n"
    "🗒 Описание:\n{description}"
)
