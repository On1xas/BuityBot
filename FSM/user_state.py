from aiogram.fsm.state import State, StatesGroup


class WelcomUser(StatesGroup):
    start = State()
    end = State()
