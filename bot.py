import asyncio


from aiogram import Bot, Dispatcher


from config.config import Config, load_config
from keyboards.menu import set_main_menu
from handlers.user_handlers import user_router

config: Config = load_config(".env")

bot: Bot = Bot(config.tg_bot.token)
dp: Dispatcher = Dispatcher()

# Регистрируем роутеры
dp.include_router(user_router)

# Регистрируем кнопку "Меню"
dp.startup.register(set_main_menu)

if __name__ == "__main__":
    asyncio.run(dp.run_polling(bot))