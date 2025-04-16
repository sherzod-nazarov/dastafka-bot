from aiogram.fsm.state import State, StatesGroup


class Sotibolish(StatesGroup):
    name = State()
    narxi = State()

class Zakaz(StatesGroup):
    contact = State()
    location = State()
    finish = State()