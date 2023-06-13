import asyncio


from aiogram import Bot, Dispatcher


from config.config import Config, load_config

config: Config = load_config(".env")

bot: Bot = Bot(config.tg_bot.token)
dp: Dispatcher = Dispatcher()



if __name__ == "__main__":
    asyncio.run(dp.run_polling(bot))