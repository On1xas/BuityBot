import datetime

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import (LEXICON_KB_ADMIN_MAIN,
                             LEXICON_RU_BUTTON,
                             LEXICON_KB_ADMIN_FSM_CreateSign_edit,
                             LEXICON_TIME_CONST)



# Главное меню для Мастер юзера
def create_kb_master_main():
    kb_admin_main = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON_KB_ADMIN_MAIN.items()]
    kb_admin_main.row(*buttons, width=2)
    return kb_admin_main.as_markup()


def button_back_main_menu():
    return [InlineKeyboardButton(text=LEXICON_RU_BUTTON["back_main_menu"], callback_data="back_main_menu")]


def create_kb_fsm_CreateSign_time():
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=value) for value in LEXICON_TIME_CONST['standart_time']]
    buttons.append(InlineKeyboardButton(text=LEXICON_RU_BUTTON["create_template_time"], callback_data="create_template_time"))
    kb.row(*buttons, width=5)
    kb.row(*button_back_main_menu())
    return kb.as_markup()


def create_kb_fsm_CreateSign_edit():
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON_KB_ADMIN_FSM_CreateSign_edit.items()]
    kb.row(*buttons, width=2)
    kb.row(*button_back_main_menu())
    return kb.as_markup()
