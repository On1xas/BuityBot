from typing import Callable, Dict, Any, Awaitable

import asyncpg
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from config.config import Config
from database.database import RequestDB


class SessionMiddleware(BaseMiddleware):
    def __init__(self, config: Config, connector: asyncpg.pool.Pool):
        super().__init__()
        self.config: Config = config
        self.connector = connector

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if data['event_from_user'].id in self.config.tg_bot.admin:
            data["config"] = self.config
        async with self.connector.acquire() as connection:
            data["database"] = RequestDB(connection=connection)
            return await handler(event, data)