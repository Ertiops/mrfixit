from aiogram import F, Router

from mrfixit.presenters.bot.dialogs.tech_request import (
    create_tech_request_dialog,
    tech_request_list_dialog,
    tech_request_view_dialog,
)
from mrfixit.presenters.bot.dialogs.tech_request.initial_handlers import (
    initiate_create_tech_request,
    initiate_get_tech_requests,
)


def register_dialogs(router: Router) -> None:
    dialog_router = Router()
    dialog_router.message(F.text.lower() == "фиксик")(initiate_create_tech_request)
    dialog_router.message(F.text.lower() == "заявки")(initiate_get_tech_requests)
    dialog_router.include_routers(
        create_tech_request_dialog,
        tech_request_list_dialog,
        tech_request_view_dialog,
    )
    router.include_router(dialog_router)
