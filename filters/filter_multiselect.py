from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class MultiSelectFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data[:2].isdigit() and 0 <= int(callback.data[:2]) < 24 and callback.data[2] == ":" and callback.data[3:].isdigit() and 0 <= int(callback.data[3:]) < 60:
            return True
        return False