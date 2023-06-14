from aiogram.filters import BaseFilter
from aiogram.types import Message

from config.config import Config


class AdminFilters(BaseFilter):
    is_admin: bool = True

    async def __call__(self, message: Message, config: Config) -> bool:
        return (message.from_user.id in config.tg_bot.admin) == True


