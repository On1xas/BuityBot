
from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import Window, Dialog


from keyboards.kb_admin import calendar

class AdminFSM_create_sign(StatesGroup):
    date = State()
    time = State()
    finish = State()

main_window = Window(
    Const("Hello, unknown person"),
    Button(calendar, id="date"),
    state=AdminFSM_create_sign.date,
)
dialog_calendar=Dialog(main_window)

class UserFSM_sing(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()