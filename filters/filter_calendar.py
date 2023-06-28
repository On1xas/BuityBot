import datetime

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class FilterCalendar(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return isinstance(callback.data, str) and (callback.data == "next_month" or callback.data == "back_month")


class FilterDateCalendar(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        try:
            valid_date = datetime.datetime.strptime(callback.data, '%d.%m.%Y')
            valid=True
        except ValueError:
            valid=False
        return isinstance(callback.data, str) and valid