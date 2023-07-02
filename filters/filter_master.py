from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from config.config import Config


# Фильтр Callback проверки ID юзера с списком ID мастеров
class MasterCallbackFilters(BaseFilter):
    is_admin: bool = True

    async def __call__(self, callback: CallbackQuery, config: Config) -> bool:
        return callback.from_user.id in config.tg_bot.admin


# Фильтр Message проверки ID юзера с списком ID мастеров
class MasterMessageFilters(BaseFilter):
    is_admin: bool = True

    async def __call__(self, message: Message, config: Config) -> bool:
        return message.from_user.id in config.tg_bot.admin


# Фильтр выбор времени в Edit_OpenSign
class SelectFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data[:2].isdigit() and 0 <= int(callback.data[:2]) < 24 and callback.data[2] == ":" and callback.data[3:].isdigit() and 0 <= int(callback.data[3:]) < 60:
            return True
        return False