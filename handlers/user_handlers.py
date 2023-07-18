from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Router
from lexicon.lexicon import LEXICON_RU


from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const


from FSM.user_state import WelcomUser
from lexicon.format_lexicon import I18NFormat, FluentKey

user_router: Router = Router()


start_user_window = Window(
    Const(FluentKey("welcome")),
    Button(Const("Useless button"), id="nothing"),
    state=WelcomUser.start
)

start_user_dialog = Dialog(start_user_window)




async def start(message: Message, dialog_manager: DialogManager):
    
    await dialog_manager.start(WelcomUser.start, mode=StartMode.RESET_STACK)










# @user_router.message(CommandStart())
# async def start(message: Message):
#     # print(message.json(exclude_none=True))
#     await message.answer(text=LEXICON_RU["start"])


@user_router.message(Command(commands=["sing"]))
async def sing(message: Message):
    await message.answer(text=LEXICON_RU["sing"])


@user_router.message(Command(commands=["my_sing"]))
async def my_sing(message: Message):
    await message.answer(text=LEXICON_RU["my_sing"])


@user_router.message(Command(commands=["history_sing"]))
async def history_sing(message: Message):
    await message.answer(text=LEXICON_RU["history_sing"])


@user_router.message(Command(commands=["portfolio"]))
async def porfolio(message: Message):
    await message.answer(text=LEXICON_RU["portfolio"])


@user_router.message(Command(commands=["price"]))
async def price(message: Message):
    await message.answer(text=LEXICON_RU["price"])
