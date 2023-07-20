from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from filters.filter_master import MasterMessageFilters
from handlers.user_handlers import start, end, any_message
from handlers.master_dialogs import master_start


def registred_user_commands(dp: Router):
    dp.message.register(start, Command(commands=["start"]) )
    #dp.message.register(any_message, StateFilter(default_state))

def registred_master_commands(dp: Router):
    dp.message.register(master_start, MasterMessageFilters(), Command(commands=["master"]))

def registred_admin_commands(dp: Router):
    pass