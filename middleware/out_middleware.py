from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from config.config import Config


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config: Config):
        self.config: Config = config

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event,
        data
    ) -> Any:
        data["config"] = self.config
        return await handler(event, data)


