from aiogram.fsm.state import State, StatesGroup


class FSM_Master_create_sign(StatesGroup):
    date = State()
    time = State()
    template = State()
    create_template = State()
    create_name_template = State()
    create_time_template = State()
    edit_template = State()
    delete_template = State()
    edit_main_template = State()
    finish = State()



class FSM_Master_edit_opensign(StatesGroup):
    date = State()
    time = State()
    entry_new_time = State()
    finish = State()


class FSM_Master_drop_opensign(StatesGroup):
    date = State()
    time = State()
    finish = State()