import logging
from typing import Callable, Awaitable, Dict, Any

#  Modules
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


logger = logging.getLogger(__name__)


#  Соединение с базой данных
class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker: async_sessionmaker):
        super().__init__()
        self.sessionmaker: AsyncSession = sessionmaker

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.sessionmaker().begin() as session:
            data["session"] = session
            return await handler(event, data)