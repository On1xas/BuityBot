from aiogram.fsm.state import StatesGroup, State


class Master_Menu(StatesGroup):
    main = State()
    check_sign = State()
    delete_sign = State()


class Master_Create_Sign(StatesGroup):
    entry_date = State()
    menu_templates = State()
    entry_time = State()
    confim_entries = State()

class Master_Delete_Sign(StatesGroup):
    select_date = State()
    multiselect_time = State()
    confim_deleting = State()

class Master_Edit_Sign(StatesGroup):
    select_date = State()
    change_date = State()
    change_time = State()
    confim_changes = State()