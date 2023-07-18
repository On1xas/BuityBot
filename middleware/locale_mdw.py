from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from fluentogram import TranslatorHub


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        hub: TranslatorHub = data.get('translator')
        # There you can ask your database for locale
        data['i18n'] = hub.get_translator_by_locale(locale=data['event_from_user'].language_code)
        return await handler(event, data)