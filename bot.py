import asyncio


import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


from config.config import Config, load_config
from keyboards.menu import set_main_menu
from handlers.user_handlers import user_router
from handlers.master_handlers import master_router
from middleware.session_middleware import SessionMiddleware


async def start_app():

    config: Config = load_config(".env")

    storage: MemoryStorage = MemoryStorage()

    bot: Bot = Bot(config.tg_bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher(storage=storage)

    # Создаём пул подключение к БД
    create_pool: asyncpg.pool.Pool = await asyncpg.create_pool(user=config.database.user, password=config.database.password, host=config.database.host, database=config.database.database)

    # Регистрируем роутеры
        # Регистрируем middleware и передаем в него конфиг и пул к для подключения к БД
    dp.update.outer_middleware(SessionMiddleware(config=config, connector=create_pool))
    dp.include_router(master_router)
    dp.include_router(user_router)

    # Регистрируем кнопку "Меню"
    dp.startup.register(set_main_menu)

    # Передаем БОТа в Диспетчер
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_app())