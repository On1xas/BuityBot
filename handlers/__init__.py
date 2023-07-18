from aiogram import Router
from aiogram.filters import CommandStart

from handlers.user_handlers import start


def registred_user_commands(dp: Router):
    dp.message.register(start, CommandStart())

def registred_master_commands(dp: Router):
    pass

def registred_admin_commands(dp: Router):
    pass