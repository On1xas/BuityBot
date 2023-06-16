from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, default_state
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON_RU
from filters.filter_admin import AdminFilters
from FSM.fsm import AdminFSM_create_sign
from keyboards.kb_admin import (create_kb_admin_main,
                                create_kb_fsm_back_admin_main,
                                create_kb_fsm_CreateSign_edit, calendar)


admin_router: Router = Router()
admin_router.message.filter(AdminFilters())


# config: Config = load_config(".env")


@admin_router.message(Command(commands=["admin"]), StateFilter(default_state))
async def admin(message: Message):
    await message.answer(text=LEXICON_RU["admin_succes"],
                         reply_markup=create_kb_admin_main())

@admin_router.callback_query(lambda callback: callback.data == "back_main_menu", ~StateFilter(default_state))
async def back_main_menu_cb(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU["admin_succes"],
                                     reply_markup=create_kb_admin_main())
    await state.clear()

@admin_router.callback_query(lambda callback: callback.data == "create_sign",
                             StateFilter(default_state))
async def FSM_create_sign_date_cb(callback: CallbackQuery, state: FSMContext):
    #print(callback.json(exclude_none=True))
    await callback.message.edit_text(text=LEXICON_RU["FSM_AdminCreateSign_date"], reply_markup=create_kb_fsm_back_admin_main)
    await state.set_state(AdminFSM_create_sign.date)
    print(await state.get_state())


@admin_router.message(StateFilter(AdminFSM_create_sign.date))
async def FSM_create_sign_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    print(await state.get_data())
    if "finish" in await state.get_data():
        await state.set_state(AdminFSM_create_sign.finish)
        storage = await state.get_data()
        await message.answer(text=f"""Были введены данные:\n\tДата: {storage['date']}\n\tВремя: {", ".join(storage['time'])}""", reply_markup=create_kb_fsm_CreateSign_edit())
    else:
        await state.set_state(AdminFSM_create_sign.time)
        print(await state.get_state())
        await message.answer(text=LEXICON_RU["FSM_AdminCreateSign_time"], reply_markup=create_kb_fsm_back_admin_main())


@admin_router.message(StateFilter(AdminFSM_create_sign.time))
async def FSM_create_sign_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text.split(","))
    await state.update_data(finish=True)
    print(await state.get_data())
    await state.set_state(AdminFSM_create_sign.finish)
    print(await state.get_state())
    storage = await state.get_data()
    await message.answer(text=f"""Были введены данные:\n\tДата: {storage['date']}\n\tВремя: {", ".join(storage['time'])}""", reply_markup=create_kb_fsm_CreateSign_edit())


@admin_router.callback_query(lambda callback: callback.data == "edit_date" or callback.data == "edit_time",
                             StateFilter(AdminFSM_create_sign.finish))
async def FSM_create_sign_edit_status_cb(callback: CallbackQuery, state: FSMContext):
    #print(callback.json(exclude_none=True))
    if callback.data == "edit_date":
        await state.set_state(AdminFSM_create_sign.date)
        await callback.message.edit_text(text=LEXICON_RU["FSM_AdminCreateSign_date"], reply_markup=create_kb_fsm_back_admin_main())
    else:
        await state.set_state(AdminFSM_create_sign.time)
        await callback.message.edit_text(text=LEXICON_RU["FSM_AdminCreateSign_time"], reply_markup=create_kb_fsm_back_admin_main())
    print(await state.get_state())


# @admin_router.callback_query(lambda callback: callback.data == "send_date",
#                              StateFilter(AdminFSM_create_sign.date))
# async def FSM_create_sign_time_cb(callback: CallbackQuery, state: FSMContext):
#     print(state.get_data())
#     await callback.message.edit_text(text=LEXICON_RU["FSM_AdminCreateSign_time"], reply_markup=create_kb_fsm_create_sing_date())
#    await state.update_data(finish=True)