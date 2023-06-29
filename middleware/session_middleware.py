from typing import Callable, Dict, Any, Awaitable

import asyncpg
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from config.config import Config


class SessionMiddleware(BaseMiddleware):
    def __init__(self, config: Config, connection_pool: asyncpg.pool.Pool):
        self.config: Config = config
        self.db_pool = connection_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:  
        if data['event_from_user'].id in self.config.tg_bot.admin:
            data["config"] = self.config
        data["database"] = self.db_pool
        return await handler(event, data)