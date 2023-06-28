from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
import asyncpg
from config.config import Config


class SessionMiddleware(BaseMiddleware):
    def __init__(self, config: Config, connection_pool: asyncpg.pool.Pool):
        self.config: Config = config
        self.db_pool = connection_pool

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event,
        data
    ) -> Any:
        data["config"] = self.config
        data["database"] = self.db_pool
        return await handler(event, data)