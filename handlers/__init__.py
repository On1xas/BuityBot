from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from handlers.user_handlers import start, end, any_message


def registred_user_commands(dp: Router):
    dp.message.register(start, Command(commands=["start"]) )
    dp.message.register(any_message, StateFilter(default_state))

def registred_master_commands(dp: Router):
    pass

def registred_admin_commands(dp: Router):
    pass