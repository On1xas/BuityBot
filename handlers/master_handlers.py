import datetime

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, default_state
from aiogram.fsm.context import FSMContext

from database.database import RequestDB
from lexicon.lexicon import LEXICON_RU
from filters.filter_master import MasterCallbackFilters, MasterMessageFilters, SelectFilter, EntryTimeFilter
from filters.filter_calendar import FilterCalendar, FilterDateCalendar
from filters.filter_multiselect import MultiSelectFilter
from FSM.fsm_master import FSM_Master_create_sign, FSM_Master_edit_opensign, FSM_Master_drop_opensign
from keyboards.kb_masters import (create_kb_master_main,
                                create_kb_fsm_CreateSign_edit,
                                kb_master_back_main_menu)
from keyboards.keyboards import kb_calendar, kb_multiselect_master_sign, kb_select_master_edit_opensign, kb_multiselect_delete_master_sign

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


## Обработка  нажатия на пустые инлайн-кноки(Декоративные)
@master_router.callback_query(lambda callback: callback.data == "empty")
async def empty(callback: CallbackQuery):
    await callback.answer()


###--------------------------------------------------------CREATE_OPENSIGN-------------------------------------------------------###


## Обработка нажатия кнопки "Создать запись" -> FSM Stage: Entry_Date
@master_router.callback_query(lambda callback: callback.data == "create_sign",
                             StateFilter(default_state))
async def FSM_create_sign_date_cb(callback: CallbackQuery, state: FSMContext):
    # Создаем запись в хранилище Месяц, Год для формирования Calendar
    await state.update_data(month=datetime.datetime.now().month, year=datetime.datetime.now().year)
    # Создаем запись в хранилище список выбранных кнопок в памяти для MultiSelect
    await state.update_data(times=[])
    await callback.message.edit_text(text=LEXICON_RU["FSM_MasterCreateSign_date"], reply_markup=kb_calendar())
    await state.set_state(FSM_Master_create_sign.date)


## Widget Calendar. Обработка нажатия кнопок пагинации в календаре.
@master_router.callback_query(FilterCalendar(), ~StateFilter(default_state))
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

## Widget Calendar. Обработка нажатия кнопки даты в календаре. FSM State -> Entry times.
@master_router.callback_query(FilterDateCalendar(), StateFilter(FSM_Master_create_sign.date))
async def date_calendar(callback: CallbackQuery, state: FSMContext, database: RequestDB):
    # Записываем дату в FSM
    await state.update_data(date=callback.data)
    # Проверяем, было редактирование данных или первичный ввод.
    if "finish" in await state.get_data():
        # Переключаемся в статус Финиш после редактирования. FSM State -> Finish.
        await state.set_state(FSM_Master_create_sign.finish)
        storage = await state.get_data()
    # Проверяем сколько временных было введено, если больше 1, подготавливаем строку.
        select_time_text = ", ".join(sorted(list(storage['times'])))
        await callback.message.edit_text(text=LEXICON_RU['FSM_MasterCreateSign_finish']. format(date=storage['date'], times=select_time_text), reply_markup=create_kb_fsm_CreateSign_edit())
    else:
    # Т.к флаг Финиш отсутсвует в состоянии - значит был первичный ввод. FSM State -> Entry times.
        await state.set_state(FSM_Master_create_sign.time)
        await callback.message.edit_text(text=LEXICON_RU["FSM_MasterCreateSign_time"], reply_markup=await kb_multiselect_master_sign(state=state, database=database))

## Widget MultiSelect. Обработка выбора времени.
@master_router.callback_query(MultiSelectFilter(), StateFilter(FSM_Master_create_sign.time))
async def cb_multiselect_time(callback: CallbackQuery, state: FSMContext, database: RequestDB):
    # Выгружаем из памяти хранилище для работы с списком
    storage: dict[str, str | list] = await state.get_data()
    # Проверяем нажатие кнопок, добавляем или убираем выбор.
    if callback.data not in storage['times']:
        storage['times'].append(callback.data)
    else:
        storage['times'].remove(callback.data)
    # Возвращаем обновленные данные в хранилище
    await state.set_data(storage)
    # Генерируем обновленную клавиатуру
    text = ", ".join(sorted(list(storage['times'])))
    await callback.message.edit_text(text=text, reply_markup=await kb_multiselect_master_sign(state=state, database=database))

## Widget MultiSelect. Обработка нажатия кнопки подтверждения выбора времени. FSM State -> Finish
@master_router.callback_query(lambda callback: callback.data == "time_selected", StateFilter(FSM_Master_create_sign.time))
async def finish_multi_select(callback: CallbackQuery, state: FSMContext, database: RequestDB):
    storage = await state.get_data()
    if "finish" not in storage:
        await state.update_data(finish=True)
    select_time_text = ", ".join(sorted(list(storage['times'])))
    await state.set_state(FSM_Master_create_sign.finish)
    await callback.message.edit_text(text=LEXICON_RU["FSM_MasterCreateSign_finish"].format(date=storage['date'], times=select_time_text), reply_markup=create_kb_fsm_CreateSign_edit())

## Обработка состояния Finish. Нажатие кнопок Изменить время, Изменить Дату.
@master_router.callback_query(lambda callback: callback.data == "edit_date" or callback.data == "edit_time",
                             StateFilter(FSM_Master_create_sign.finish))
async def FSM_create_sign_edit_status_cb(callback: CallbackQuery, state: FSMContext, database: RequestDB):
    if callback.data == "edit_date":
        await state.set_state(FSM_Master_create_sign.date)
        await callback.message.edit_text(text=LEXICON_RU["FSM_MasterCreateSign_date"], reply_markup=kb_calendar())
    else:
        await state.set_state(FSM_Master_create_sign.time)
        await callback.message.edit_text(text=LEXICON_RU["FSM_MasterCreateSign_time"], reply_markup=await kb_multiselect_master_sign(state=state, database=database))

## Обработка состояния Finish. Нажание кнопки Создать запись.
@master_router.callback_query(lambda callback: callback.data == "save",
                             StateFilter(FSM_Master_create_sign.finish))
async def FSM_create_sign_time_cb(callback: CallbackQuery, state: FSMContext, database: RequestDB):
    storage = await state.get_data()
    print(storage)
    await database.set_opensign(storage['date'], storage['times'])
    await state.clear()
    await callback.message.edit_text(text="Запись создана!", reply_markup=create_kb_master_main())

## default state. Обработка нажатия кнопки Проверить записи
@master_router.callback_query(lambda callback: callback.data == "check_sign", StateFilter(default_state))
async def check_sign(callback: CallbackQuery, database: RequestDB):
    open_sign: dict[str, list] = await database.get_opensign()
    text=LEXICON_RU['check_open_sign']
    for key, value in sorted(open_sign.items(), key=lambda x: datetime.datetime.strptime(x[0], '%d.%m.%Y')):
        value.sort()
        text+="\t\t<u>{date}</u> - <i>{times}</i>\n".format(date=key, times=", ".join(value))
    await callback.message.edit_text(text=text, reply_markup=create_kb_master_main())

## FSM_Master_edit_opensign. Обработка нажатия кнопки Изменить запись
@master_router.callback_query(lambda callback: callback.data == "edit_sign", StateFilter(default_state))
async def edit_sign(callback: CallbackQuery, state: FSMContext, database: RequestDB):
    # Инициализация переменных для работы с MultiWidget и Calendar
    await state.update_data(month=datetime.datetime.now().month, year=datetime.datetime.now().year)
    await state.update_data(times=[])
    await state.set_state(FSM_Master_edit_opensign.date)
    await callback.message.edit_text(text="Выберите дату в которой хотите изменить запись", reply_markup=kb_calendar())             ### ИЗМЕНИТЬ ОБРАБОТКУ ТЕКСТА


###--------------------------------------------------------EDIT_OPENSIGN-------------------------------------------------------###


## FSM_Master_edit_opensign - Widget Calendar. Обработка нажатия кнопки даты в календаре. FSM State -> Entry times.
@master_router.callback_query(FilterDateCalendar(), StateFilter(FSM_Master_edit_opensign.date))
async def date_calendar(callback: CallbackQuery, state: FSMContext, database: RequestDB):
    # Записываем дату в FSM
    await state.update_data(date=callback.data)
    # Проверяем, было редактирование данных или первичный ввод.
    if await database.get_opensign(value=callback.data):
        # FSM State -> Entry times.
        await state.set_state(FSM_Master_edit_opensign.time)
        await callback.message.edit_text(text=LEXICON_RU["FSM_MasterCreateSign_time"], reply_markup=await kb_select_master_edit_opensign(state=state, database=database))
    else:
        # Выдаём кнопку возрат в главное меню
        await callback.message.edit_text(text="К сожалению на данную дату нет запланированных записей", reply_markup=kb_master_back_main_menu())


## FSM_Master_edit_opensign - Widget Select. Обработка выбора времени.
@master_router.callback_query(SelectFilter(), StateFilter(FSM_Master_edit_opensign.time))
async def cb_select_time(callback: CallbackQuery, state: FSMContext, database: RequestDB):
    await state.update_data(old_time=callback.data)
    await state.set_state(FSM_Master_edit_opensign.entry_new_time)
    await callback.message.edit_text(text="Введите время которое хотите изменить")                                  ### ИЗМЕНИТЬ ОБРАБОТКУ ТЕКСТА





## FSM_Master_edit_opensign - Обработка ввода нового времени
@master_router.message(EntryTimeFilter(), StateFilter(FSM_Master_edit_opensign.entry_new_time))
async def cb_select_entry_new_time(message: Message, state: FSMContext, database: RequestDB):
    # Сохраняем текстовый ввод
    await state.update_data(new_time=message.text)
    # Обновляем данные в БД
    storage = await state.get_data()
    await database.update_opensign(date_update=storage['date'], old_time=storage['old_time'], new_time=storage['new_time'])
    # Удаляем сообщение с введенным тектсом
    await message.delete()
    await message.answer(text=f"Запись изменена на {message.text}", reply_markup=create_kb_master_main())                                                  ### ИЗМЕНИТЬ ОБРАБОТКУ ТЕКСТА
    await state.clear()

## FSM_Master_edit_opensign - Обработка ввода некоректного текста
@master_router.message(StateFilter(FSM_Master_edit_opensign.entry_new_time))
async def cb_select_entry_new_time_fail(message: Message, state: FSMContext, database: RequestDB):
    await message.answer(text=f"Неверный ввод")                                                                     ### ИЗМЕНИТЬ ОБРАБОТКУ ТЕКСТА

###--------------------------------------------------------DELETE_OPENSIGN-------------------------------------------------------###


## FSM_Master_drop_opensign - Обработка нажатия кнопки "Удалить запись" -> FSM Stage: Entry_Date
@master_router.callback_query(lambda callback: callback.data == "delete_sign",
                             StateFilter(default_state))
async def FSM_drop_opensign_cb(callback: CallbackQuery, state: FSMContext):
    # Создаем запись в хранилище Месяц, Год для формирования Calendar
    await state.update_data(month=datetime.datetime.now().month, year=datetime.datetime.now().year)
    # Создаем запись в хранилище список выбранных кнопок в памяти для MultiSelect
    await state.update_data(times=[])
    await callback.message.edit_text(text=LEXICON_RU["FSM_MasterCreateSign_date"], reply_markup=kb_calendar())
    await state.set_state(FSM_Master_drop_opensign.date)

## FSM_Master_drop_opensign  Widget Calendar. Обработка нажатия кнопки даты в календаре. FSM State -> Entry times.      #### СДЕЛАТЬ ПРОВЕРКУ НА ПРИСУТСВИЕ ДАТЫ
@master_router.callback_query(FilterDateCalendar(), StateFilter(FSM_Master_drop_opensign.date))
async def date_calendar_drop_opensign(callback: CallbackQuery, state: FSMContext, database: RequestDB):
    if await database.get_opensign(value=callback.data):
        # Записываем дату в FSM
        await state.update_data(date=callback.data)
        # FSM State -> Entry times.
        await state.set_state(FSM_Master_drop_opensign.time)
        await callback.message.edit_text(text=LEXICON_RU["FSM_MasterCreateSign_time"], reply_markup=await kb_multiselect_delete_master_sign(state=state, database=database))
    else:
        await callback.message.edit_text(text="Не записей на этот день", reply_markup=kb_master_back_main_menu())

## FSM_Master_drop_opensign Widget MultiSelect. Обработка выбора времени.
@master_router.callback_query(MultiSelectFilter(), StateFilter(FSM_Master_drop_opensign.time))
async def cb_multiselect_time(callback: CallbackQuery, state: FSMContext, database: RequestDB):
    # Выгружаем из памяти хранилище для работы с списком
    storage: dict[str, str | list] = await state.get_data()
    # Проверяем нажатие кнопок, добавляем или убираем выбор.
    if callback.data not in storage['times']:
        storage['times'].append(callback.data)
    else:
        storage['times'].remove(callback.data)
    # Возвращаем обновленные данные в хранилище
    await state.set_data(storage)
    # Формируем текст в записимости от выбранных кнопок
    if storage['times']:
        text = ", ".join(sorted(list(storage['times'])))
    else:
        text = "Нет выбранных записей"
    # Генерируем обновленную клавиатуру
    await callback.message.edit_text(text=text, reply_markup=await kb_multiselect_delete_master_sign(state=state, database=database))

## FSM_Master_drop_opensign Widget MultiSelect. Обработка нажатия кнопки подтверждения выбора времени. FSM State -> Finish
@master_router.callback_query(lambda callback: callback.data == "time_selected", StateFilter(FSM_Master_drop_opensign.time))
async def finish_multi_select_drop_opensign(callback: CallbackQuery, state: FSMContext, database: RequestDB):
    storage = await state.get_data()
    for time in storage['times']:
        await database.delete_opensign(storage["date"], time)
    # select_time_text = ", ".join(sorted(list(storage['times'])))
    await callback.message.edit_text(text="Что то удалилось ", reply_markup=create_kb_master_main())
    await state.clear()