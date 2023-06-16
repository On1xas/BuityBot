from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Router
from aiogram_dialog import DialogManager, StartMode
from lexicon.lexicon import LEXICON_RU
from FSM.fsm import AdminFSM_create_sign
user_router: Router = Router()


# @user_router.message(CommandStart())
# async def start(message: Message):
#     # print(message.json(exclude_none=True))
#     await message.answer(text=LEXICON_RU["start"])

@user_router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminFSM_create_sign.date,
                               mode=StartMode.RESET_STACK)

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
