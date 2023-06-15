from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


from lexicon.lexicon import LEXICON_KB_ADMIN_MAIN, LEXICON_KB_ADMIN_FSM_Create_sign_date


def create_kb_admin_main():
    kb_admin_main = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON_KB_ADMIN_MAIN.items()]
    kb_admin_main.row(*buttons, width=2)
    return kb_admin_main.as_markup()


def create_kb_fsm_create_sing_date():
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON_KB_ADMIN_FSM_Create_sign_date.items()]
    kb.row(*buttons, width=1)
    return kb.as_markup()