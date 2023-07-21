from aiogram.fsm.state import StatesGroup, State


class Master_Menu(StatesGroup):
    main = State()
    check_sign = State()


class Master_Create_Sign(StatesGroup):
    entry_date = State()
    menu_templates = State()
    entry_time = State()
    confim_entries = State()