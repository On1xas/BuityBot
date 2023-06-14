from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from lexicon.lexicon import LEXICON_RU
from config.config import Config, load_config


admin_router: Router = Router()

config: Config = load_config(".env")


@admin_router.message(Command(commands=["admin"]))
async def admin(message: Message):
    print(message.json(exclude_none=True))
    print(message.from_user.id, type(message.from_user.id))
    print(config.tg_bot.admin)
    if message.from_user.id in config.tg_bot.admin:
        await message.answer(text=LEXICON_RU["admin_succes"])
    else:
        await message.answer(text=LEXICON_RU["admin_denied"])
