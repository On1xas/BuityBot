from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from config.config import Config
from config.roles import Roles


class RoleMiddleware(BaseMiddleware):
    def __init__(self, admins: list, masters: list):
        super().__init__()
        self.admins: list = admins
        self.masters: list = masters

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if data['event_from_user'].id in self.admins:
            data["role"] = Roles.ADMIN
            print("ADmin")
        elif data['event_from_user'].id in self.masters:
            data["role"] = Roles.MASTER
            print("Master")
        else:
            data["role"] = Roles.USER
            print("user")
        return await handler(event, data)