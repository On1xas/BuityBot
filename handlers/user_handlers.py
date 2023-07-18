from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import Router
from lexicon.lexicon import LEXICON_RU


from aiogram_dialog import Dialog, Window, DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const
from aiogram.fsm.context import FSMContext

from FSM.user_state import WelcomUser
from lexicon.format_lexicon import FluentText
from lexicon.runner import runner

user_router: Router = Router()

async def to_second(callback: CallbackQuery, button: Button,
                    manager: DialogManager):
    print(manager.start_data)
    state = manager.start_data.get("state")
    print(await state.get_state())
    await manager.switch_to(WelcomUser.end)

start_user_window = Window(
    FluentText(runner.welcome()),
    Button(Const("Useless button"), id="nothing", on_click=to_second),
    state=WelcomUser.start
)



async def start(message: Message, dialog_manager: DialogManager, state: FSMContext):
    await dialog_manager.start(WelcomUser.start, mode=StartMode.RESET_STACK, data=dialog_manager.middleware_data)

async def any_message( message: Message, dialog_manager: DialogManager, state: FSMContext, bot: Bot):
    await message.delete()
#  chat_id=message.chat.id, message_id=message.from_user.id
end_user_window = Window(
    FluentText(runner.end()),
    Row(
        Button(Const("Stop bot"), id="stop"),
        Button(Const("Continue"), id="continue")
    ),
    state=WelcomUser.end
)

async def end(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.answer_callback()



user_dialog = Dialog(start_user_window, end_user_window)

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
