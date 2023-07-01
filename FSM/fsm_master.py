
from aiogram.fsm.state import State, StatesGroup


class FSM_Master_create_sign(StatesGroup):
    date = State()
    time = State()
    finish = State()



class FSM_Master_edit_opensign(StatesGroup):
    date = State()
    time = State()
    finish = State()


class FSM_Master_drop_opensign(StatesGroup):
    date = State()
    time = State()
    finish = State()