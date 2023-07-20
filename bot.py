import asyncio
import os

import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from config.config import Config, load_config
from keyboards.menu import set_main_menu
from handlers.user_handlers import user_router
from handlers.master_handlers import master_router
from middleware.session_middleware import SessionMiddleware
from middleware.role_mdw import RoleMiddleware
from middleware.locale_mdw import TranslatorRunnerMiddleware
from middleware.db_mdw import DbSessionMiddleware
from lexicon.translator import translator_hub
from database.base import async_create_engine
from handlers import registred_user_commands, registred_master_commands, registred_admin_commands
from handlers.user_handlers import user_dialog
from handlers.master_dialogs import master_dialog, master_create_sign_dialog

async def start_app():

    config: Config = load_config(".env")
    storage: MemoryStorage = MemoryStorage()
    #print(f"{os.getenv('DRIVER')}://{os.getenv('HOST')}:{os.getenv('PORT')}@{os.getenv('USER_DB')}:{os.getenv('PASSWORD_DB')}/{os.getenv('DATABASE')}")
    bot: Bot = Bot(config.tg_bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher(storage=storage)

    # Создаём пул подключение к БД
    # create_pool: asyncpg.pool.Pool = await asyncpg.create_pool(
    #     user=config.database.user,
    #     password=config.database.password,
    #     host=config.database.host,
    #     database=config.database.database
    #        )
    connect_sessionmaker = await async_create_engine(
        driver=config.database.driver,
        host=config.database.host,
        port=config.database.port,
        username=config.database.user,
        password=config.database.password,
        database=config.database.database
    )
    # Регистрируем роутеры
    # Регистрируем middleware и передаем в него конфиг и пул к для подключения к БД
    dp.callback_query.middleware(SessionMiddleware())
    dp.update.middleware(RoleMiddleware(
        admins=config.tg_bot.admins,
        masters=config.tg_bot.masters)
        )
    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.update.middleware(DbSessionMiddleware(connect_sessionmaker))

    # dp.update.outer_middleware(SessionMiddleware(config=config, connector=create_pool))



    registred_master_commands(dp)
    registred_admin_commands(dp)
    registred_user_commands(dp)
    dp.include_router(user_dialog)
    dp.include_router(master_dialog)
    dp.include_router(master_create_sign_dialog)
    setup_dialogs(dp)


    # dp.include_router(master_router)
    # dp.include_router(user_router)

    # Регистрируем кнопку "Меню"
    dp.startup.register(set_main_menu)

    # Передаем БОТа в Диспетчер
    await dp.start_polling(bot, translator=translator_hub, allowed_updates=[])

if __name__ == "__main__":
    asyncio.run(start_app())
