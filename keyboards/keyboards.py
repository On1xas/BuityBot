import datetime
import calendar


from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.fsm.context import FSMContext


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