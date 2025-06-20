from aiogram.fsm.state import State, StatesGroup


class TechRequestListState(StatesGroup):
    view = State()


class CreateTechRequestState(StatesGroup):
    building = State()
    category = State()
    title = State()
    description = State()
    photo = State()
    confirm = State()


class GetTechRequestState(StatesGroup):
    view = State()
