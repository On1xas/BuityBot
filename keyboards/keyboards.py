import datetime
import calendar


from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON_RU_MULTI_SELECT_BUTTON, LEXICON_RU_BUTTON
from database.database import RequestDB
from keyboards.kb_masters import button_back_main_menu



def kb_calendar(month=datetime.datetime.now().month,
                year=datetime.datetime.now().year):
    range_month = calendar.monthrange(month=month, year=year)
    first_week_day = range_month[0]
    days = [day for day in range(1, range_month[1]+1)]
    kb = InlineKeyboardBuilder()
    week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    pagination_button = [InlineKeyboardButton(text="<<<",
                                              callback_data="back_month")]+[InlineKeyboardButton(text=f"{datetime.datetime(month=month, year=year, day=1).strftime('%b %Y')}", callback_data="empty")]+[InlineKeyboardButton(text=">>>",callback_data="next_month")]
    kb.row(*pagination_button, width=3)
    kb.row(*[InlineKeyboardButton(text=week_day, callback_data="empty") for week_day in week])
    if first_week_day != 0:
        rows = []+[InlineKeyboardButton(text=" ", callback_data="empty")]*first_week_day
    else:
        rows = []
    while len(days) != 0:
        while len(rows) != 7:
            if len(days) == 0:
                break
            day = days.pop(0)
            rows.append(InlineKeyboardButton(text=day, callback_data=f"{str(day).rjust(2, '0')}.{str(month).rjust(2, '0')}.{year}"))
        if len(days) != 0:
            kb.row(*rows, width=7)
            rows = []
    if len(rows) != 7:
        rows += [InlineKeyboardButton(text=" ",callback_data="empty")]*(7-len(rows))
        kb.row(*rows, width=7)
    else:
        kb.row(*rows, width=7)
    return kb.as_markup()


async def kb_multiselect_master_sign(state: FSMContext, database: RequestDB):
    kb = InlineKeyboardBuilder()
    selected = await state.get_data()
    main_button = []
    print(selected)
    for time in LEXICON_RU_MULTI_SELECT_BUTTON['times_to_sign']:
        if selected and time in selected['times']:
            main_button.append(InlineKeyboardButton(text=f"[{time}]",
                               callback_data=time))
        else:
            main_button.append(InlineKeyboardButton(text=f"{time}",
                               callback_data=time))
    kb.row(*main_button, width=5)
    kb.row(InlineKeyboardButton(text=LEXICON_RU_BUTTON["time_selected"],
                                callback_data="time_selected"), width=1)
    return kb.as_markup()

async def kb_select_master_edit_opensign(state: FSMContext, database: RequestDB):
    kb = InlineKeyboardBuilder()
    selected = await state.get_data()
    db_open_sign = await database.get_opensign(value=selected['date'])
    main_button = []
    for time in sorted(db_open_sign[selected['date']]):
            main_button.append(InlineKeyboardButton(text=f"Изменить запись {selected['date']} - {time}",
                                callback_data=time))
    kb.row(*main_button, width=1)
    kb.row(*button_back_main_menu())
    return kb.as_markup()

async def kb_multiselect_delete_master_sign(state: FSMContext, database: RequestDB):
    kb = InlineKeyboardBuilder()
    selected = await state.get_data()
    main_button = []
    print(selected)
    db_open_sign = await database.get_opensign(value=selected['date'])
    for time in sorted(db_open_sign[selected['date']]):
        if selected and time in selected['times']:
            main_button.append(InlineKeyboardButton(text=f"Удалить запись [{time}]",
                                callback_data=time))
        else:
            main_button.append(InlineKeyboardButton(text=f"Удалить запись  {time}",
                                callback_data=time))
    kb.row(*main_button, width=1)
    kb.row(InlineKeyboardButton(text=LEXICON_RU_BUTTON["time_selected"],
                                    callback_data="time_selected"), width=1)
    return kb.as_markup()