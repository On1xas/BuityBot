import datetime

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.keyboards import generate_calendar
from lexicon.lexicon import (LEXICON_KB_ADMIN_MAIN,
                             LEXICON_RU_BUTTON,
                             LEXICON_KB_ADMIN_FSM_CreateSign_edit,
                             LEXICON_TIME_CONST)




def create_kb_admin_main():
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



def create_kb_calendar():
    kb=InlineKeyboardBuilder()
    week=["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс" ]
    kb.row(*[InlineKeyboardButton(text=week_day, callback_data="empty") for week_day in week])
    days=[(datetime.datetime.now()+datetime.timedelta(days=shift)).strftime("%d.%m") for shift in range(0,31)]
    print(days)
    if datetime.datetime.now().weekday() != 6:
        rows=[]+[InlineKeyboardButton(text=" ",callback_data="empty")]*(datetime.datetime.now().weekday())
    while len(days) != 0:
        while len(rows) != 7:
            if len(days) == 0:
                break
            day = days.pop(0)
            rows.append(InlineKeyboardButton(text=day, callback_data=day))
        if len(days) != 0:
            kb.row(*rows, width=7)
            rows=[]
    if len(rows) !=7:
        rows+=[InlineKeyboardButton(text=" ",callback_data="empty")]*(7-len(rows))
        kb.row(*rows, width=7)
    kb.row(*button_back_main_menu())
    return kb.as_markup()
