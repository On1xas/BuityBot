from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from config.config import Config
from config.roles import Roles

# Фильтр Callback проверки ID юзера с списком ID мастеров
class MasterCallbackFilters(BaseFilter):
    is_admin: bool = True

    async def __call__(self, callback: CallbackQuery, config: Config) -> bool:
        return callback.from_user.id in config.tg_bot.admins


# Фильтр Message проверки ID юзера с списком ID мастеров
class MasterMessageFilters(BaseFilter):
    is_admin: bool = True

    async def __call__(self, message: Message, role: Roles) -> bool:
        print(role)
        if role == Roles.ADMIN or role == Roles.MASTER:
            return True
        return False


# Фильтр выбор времени в Edit_OpenSign
class SelectFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data[:2].isdigit() and 0 <= int(callback.data[:2]) < 24 and callback.data[2] == ":" and callback.data[3:].isdigit() and 0 <= int(callback.data[3:]) < 60:
            return True
        return False

# Фильтр выбор времени в Edit_OpenSign
class EntryTimeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text[:2].isdigit() and 0 <= int(message.text[:2]) < 24 and message.text[2] == ":" and message.text[3:].isdigit() and 0 <= int(message.text[3:]) < 60:
            return True
        return False


# Фильтр ввода имени нового шаблона
class EntryNameTemplateFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if len(message.text) > 15:
            return False
        return True


# Фильтр ввода времени нового шаблона
class EntryTimeTemplateFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        times = message.text.split(",")
        return all([True if time[:2].isdigit() and 0 <= int(time[:2]) < 24 and time[2] == ":" and time[3:].isdigit() and 0 <= int(time[3:]) < 60 else False for time in times])