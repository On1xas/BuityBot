
from aiogram.fsm.state import State, StatesGroup


class AdminFSM_create_sign(StatesGroup):
    date = State()
    time = State()

class UserFSM_sing(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()