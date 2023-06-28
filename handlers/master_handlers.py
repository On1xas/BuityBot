import datetime

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, default_state
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON_RU
from filters.filter_master import MasterCallbackFilters,MasterMessageFilters
from filters.filter_calendar import FilterCalendar, FilterDateCalendar
from FSM.fsm_master import FSM_Master_create_sign
from keyboards.kb_masters import (create_kb_master_main,
                                create_kb_fsm_CreateSign_edit,
                                create_kb_fsm_CreateSign_time)
from keyboards.keyboards import kb_calendar


master_router: Router = Router()
master_router.callback_query.filter(MasterCallbackFilters())
master_router.message.filter(MasterMessageFilters())


## Обработка команды /master
@master_router.message(Command(commands=["master"]), StateFilter(default_state))
async def admin(message: Message):
    await message.answer(text=LEXICON_RU["master_succes"],
                         reply_markup=create_kb_master_main())

## Обработка нажатия кнопки назад в Главное меню Администратора - СБРАСЫВАЕТ СОСТОЯНИЕ FSM_Master_create_sign
@master_router.callback_query(lambda callback: callback.data == "back_main_menu", ~StateFilter(default_state))
async def back_main_menu_cb(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU["master_succes"],
                                     reply_markup=create_kb_master_main())
    await state.clear()

## Обработка нажатия кнопки "Создать запись"
@master_router.callback_query(lambda callback: callback.data == "create_sign",
                             StateFilter(default_state))
async def FSM_create_sign_date_cb(callback: CallbackQuery, state: FSMContext):
    await state.update_data(month=datetime.datetime.now().month, year=datetime.datetime.now().year)
    await callback.message.edit_text(text=LEXICON_RU["FSM_AdminCreateSign_date"], reply_markup=kb_calendar())
    await state.set_state(FSM_Master_create_sign.date)

## Обработка  нажатия на пустые инлайн-кноки(Декоративные)
@master_router.callback_query(lambda callback: callback.data == "empty")
async def empty(callback: CallbackQuery):
    await callback.answer()



## Обработка нажатия кнопок пагинации в календаре, в статусе машины ДАТА

@master_router.callback_query(FilterCalendar(), StateFilter(FSM_Master_create_sign.date))
async def next_back_month(callback: CallbackQuery, state: FSMContext):
    user = await state.get_data()
    if callback.data == "next_month":
        user["month"] += 1
        if user["month"] > 12:
            user["month"] = 1
            user["year"] += 1
    if callback.data == "back_month":
        user["month"] -= 1
        if user["month"] <= 0:
            user["month"] = 12
            user["year"] -= 1
    await state.set_data(user)
    await callback.message.edit_text(text="Ваш выбор {}.{}".format(user["month"], user["year"]), reply_markup=kb_calendar(month=user["month"], year=user["year"]))

@master_router.callback_query(lambda callback: callback.data != "empty", StateFilter(FSM_Master_create_sign.date))
async def FSM_create_sign_date(callback: CallbackQuery, state: FSMContext):
    await state.update_data(date=callback.data)
    if "finish" in await state.get_data():
        await state.set_state(FSM_Master_create_sign.finish)
        storage = await state.get_data()
        if len(storage["time"])//5 > 1:
            storage["time"]=", ".join(storage['time'])
        await callback.message.edit_text(text=f"""Были введены данные:\n\tДата: {storage['date']}\n\tВремя: {storage['time']}""", reply_markup=create_kb_fsm_CreateSign_edit())
    else:
        await state.set_state(FSM_Master_create_sign.time)
        await callback.message.edit_text(text=LEXICON_RU["FSM_AdminCreateSign_time"], reply_markup=create_kb_fsm_CreateSign_time())


@master_router.callback_query(StateFilter(FSM_Master_create_sign.time))
async def FSM_create_sign_time(callback: CallbackQuery, state: FSMContext):
    await state.update_data(time=callback.data)
    await state.update_data(finish=True)
    await state.set_state(FSM_Master_create_sign.finish)
    storage = await state.get_data()
    if len(storage["time"])//5 > 1:
        storage["time"]=", ".join(storage['time'])
    await callback.message.edit_text(text=f"""Были введены данные:\n\tДата: {storage['date']}\n\tВремя: {storage['time']}""", reply_markup=create_kb_fsm_CreateSign_edit())


@master_router.callback_query(lambda callback: callback.data == "edit_date" or callback.data == "edit_time",
                             StateFilter(FSM_Master_create_sign.finish))
async def FSM_create_sign_edit_status_cb(callback: CallbackQuery, state: FSMContext):
    #print(callback.json(exclude_none=True))
    if callback.data == "edit_date":
        await state.set_state(FSM_Master_create_sign.date)
        await callback.message.edit_text(text=LEXICON_RU["FSM_AdminCreateSign_date"], reply_markup=create_kb_calendar())
    else:
        await state.set_state(FSM_Master_create_sign.time)
        await callback.message.edit_text(text=LEXICON_RU["FSM_AdminCreateSign_time"], reply_markup=create_kb_fsm_CreateSign_time())


# @admin_router.callback_query(lambda callback: callback.data == "send_date",
#                              StateFilter(AdminFSM_create_sign.date))
# async def FSM_create_sign_time_cb(callback: CallbackQuery, state: FSMContext):
#     print(state.get_data())
#     await callback.message.edit_text(text=LEXICON_RU["FSM_AdminCreateSign_time"], reply_markup=create_kb_fsm_create_sing_date())
#    await state.update_data(finish=True)