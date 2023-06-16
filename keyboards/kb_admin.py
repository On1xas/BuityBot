from datetime import date

from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar
from aiogram_dialog import Dialog

from lexicon.lexicon import (LEXICON_KB_ADMIN_MAIN,
                             LEXICON_KB_ADMIN_FSM_back_admin_main,
                             LEXICON_KB_ADMIN_FSM_CreateSign_edit)



async def on_date_selected(callback: CallbackQuery, widget,
                           manager: DialogManager, selected_date: date):
    await callback.answer(str(selected_date))

calendar = Calendar(id='calendar', on_click=on_date_selected)


def create_kb_admin_main():
    kb_admin_main = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON_KB_ADMIN_MAIN.items()]
    kb_admin_main.row(*buttons, width=2)
    return kb_admin_main.as_markup()


def create_kb_fsm_back_admin_main():
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON_KB_ADMIN_FSM_back_admin_main.items()]
    kb.row(*buttons, width=1)
    return kb.as_markup()

def create_kb_fsm_CreateSign_date():
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON_KB_ADMIN_FSM_back_admin_main.items()]
    kb.row(*buttons, width=1)
    return kb.as_markup()

def create_kb_fsm_CreateSign_edit():
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON_KB_ADMIN_FSM_CreateSign_edit.items()]
    kb.row(*buttons, width=2)
    kb.row(*[InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON_KB_ADMIN_FSM_back_admin_main.items()])
    return kb.as_markup()