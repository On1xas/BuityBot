from typing import Callable, Dict, Any, Awaitable

import asyncpg
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery

from config.config import Config
from database.database import RequestDB


class SessionMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        print(event)
        return await handler(event, data)