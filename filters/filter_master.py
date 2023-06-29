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
