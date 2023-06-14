from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon import LEXICON_COMMANDS_RU


async def set_main_menu(bot: Bot):
    main_menu = [BotCommand(command=key, description=value) for key, value in LEXICON_COMMANDS_RU.items()]
    print("Кнопка Меню успешно инициализирована")
    await bot.set_my_commands(main_menu)
