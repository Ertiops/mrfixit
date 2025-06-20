from aiogram_dialog import Dialog

from mrfixit.presenters.bot.dialogs.tech_request import (
    windows as tech_request_windows,
)

create_tech_request_dialog = Dialog(
    tech_request_windows.building_selection_window(),
    tech_request_windows.category_selection_window(),
    tech_request_windows.title_input_window(),
    tech_request_windows.description_input_window(),
    tech_request_windows.photo_input_window(),
    tech_request_windows.request_preview_window(),
)

tech_request_list_dialog = Dialog(
    tech_request_windows.tech_request_list_window(),
)
tech_request_view_dialog = Dialog(
    tech_request_windows.tech_request_view_window(),
)
