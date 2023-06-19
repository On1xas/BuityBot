from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.kb_test import KB_Calendar


TOKEN = "6095290433:AAE6t3nVcf9nNGOKdqVLZwobmy7hJuy-DWI"

bot: Bot = Bot(TOKEN)
dp: Dispatcher = Dispatcher()


if __name__ == "__main__":
    dp.run_polling(bot)