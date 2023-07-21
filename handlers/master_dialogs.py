from datetime import date

from aiogram_dialog import Dialog, DialogManager, StartMode, Window, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Multiselect, Calendar, Column, Group
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import Message, CallbackQuery, ContentType


from FSM.master_state import Master_Create_Sign, Master_Menu
from services.db_service import Master
###===============Handlers======================###
async def master_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Master_Menu.main, mode=StartMode.RESET_STACK, show_mode=ShowMode.AUTO)


async def master_entry_time_manually(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    async def check_times_sign_input(message: str):
        times=message.split(",")
        if len(times)>8:
            return False
        return all([True if len(time) == 5 and time[:2].isdigit() and 0 <= int(time[:2]) < 24 and time[2] == ":" and time[3:].isdigit() and 0 <= int(time[3:]) < 60 else False for time in times])
    if await check_times_sign_input(message=message.text):
        print("In Handler")

        dialog_manager.dialog_data["times"]=dialog_manager.dialog_data.get("times", message.text.split(","))
        dialog_manager.dialog_data["status_state"] = "confim"
        print("Time Select", dialog_manager.dialog_data)
        await dialog_manager.switch_to(Master_Create_Sign.confim_entries)
    else:
        await message.answer("Ввел хуйню")

###===============Clikers======================###

async def to_main_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.done()
    await manager.start(Master_Menu.main, mode=StartMode.RESET_STACK, show_mode=ShowMode.AUTO)

async def to_check_opensign(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Master_Menu.check_sign, show_mode=ShowMode.AUTO)

async def to_create_sign_entry_date(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.done()
    await manager.start(state=Master_Create_Sign.entry_date, mode=StartMode.NORMAL)
    print("Create Dialog Data", manager.dialog_data)
    manager.dialog_data["date"] = manager.dialog_data.get("date", date.today())
    manager.dialog_data["status_state"] = manager.dialog_data.get("status_state", None)
    print(manager.dialog_data)


async def to_create_sign_entry_time(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(state=Master_Create_Sign.entry_time)

async def to_create_sign_change_entry_date(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(state=Master_Create_Sign.entry_date)

async def on_date_selected(callback: CallbackQuery, widget,
                           manager: DialogManager, selected_date: date):

    if selected_date < date.today():
        await callback.answer(text=f"{str(selected_date)} - уже прошла, выберите актуальную")
    else:
        manager.dialog_data["date"]=selected_date
        print("Date Select", manager.dialog_data)
        if manager.dialog_data["status_state"] == "confim":
            await manager.switch_to(Master_Create_Sign.confim_entries)
        else:
            manager.dialog_data["date"]=selected_date
            await manager.switch_to(Master_Create_Sign.menu_templates)
async def to_save_opensign(callback: CallbackQuery, button: Button, manager: DialogManager):
    print(manager.middleware_data)
    session: Master = manager.middleware_data['session']
    await session.set_open_sign(master_id=callback.from_user.id, date=manager.dialog_data['date'], times=manager.dialog_data['times'])
    await manager.done()
    await manager.start(Master_Menu.main, mode=StartMode.RESET_STACK, show_mode=ShowMode.AUTO)

###===============Getters======================###
async def get_data(dialog_manager: DialogManager, **kwargs):

    return dialog_manager.dialog_data

async def getter_opensign(dialog_manager: DialogManager, **kwargs):
    session: Master = dialog_manager.middleware_data['session']
    id = dialog_manager.middleware_data['event_from_user'].id
    result = await session.get_open_sign()
    text = ""
    for date, times in result[id].items():
        t=", ".join(sorted(times))
        text += f"\n\t\t{date} - {t}"
    return {"text": text}

###===============When======================###

###===============Keyboards======================###

kb_main_menu = Group(
        Row(
            Button(Const("Создать запись"), id="create_sign", on_click=to_create_sign_entry_date),
            Button(Const("Изменить запись"), id="edit_sign")
        ),
            Row(
            Button(Const("Проверить запись"), id="check_sign", on_click=to_check_opensign),
            Button(Const("Удалить запись"), id="delete_sign")
        ))

###===============Windows======================###
master_main_menu = [
    Window(
        Const("Вы находите в 🎈 главном меню мастера:"),
        kb_main_menu,
        state=Master_Menu.main
        ),
    Window(
        Format("Свободные записи:\n{text}"),
        kb_main_menu,
        state=Master_Menu.check_sign,
        getter=getter_opensign
        )
    ]

calendar = Calendar(id='calendar', on_click=on_date_selected)

create_sign = [
    Window(
        Const("Выберите дату"),
        calendar,
        state=Master_Create_Sign.entry_date,
        getter=get_data
    ),
    Window(
        Const("Выберите время"),
        Row(
            Button(Const("Создать шаблон"), id="create_template"),
            Button(Const("Изменить шаблон"), id="edit_template"),
            Button(Const("Удалить шаблон"), id="delete_template")
        ),
        Button(Const("Ввести время вручную"), id="entry_time_manually", on_click=to_create_sign_entry_time),
        Button(Const("Тут Будет Multiselect из времени основного шаблона"), id="tempid"),
        Column(
            Button(Const("Шаблон 1"),id="template_1"),
            Button(Const("Шаблон 2"),id="template_2"),
        ),
        Button(Const("Вернуться в главное меню"), id="back_main_menu", on_click=to_main_menu),
        state=Master_Create_Sign.menu_templates
    ),
    Window(
        Const("Вводи как я сказал. 11:00 если несколько таймеров, то перечисляй через запятую без пробелов - 11:00,12:00."),
        MessageInput(master_entry_time_manually, content_types=[ContentType.TEXT]),
        state=Master_Create_Sign.entry_time
    ),
    Window(
        Const("Все заебись"),
        Row(
            Button(Const("Изменить Дату"), id="change_date", on_click=to_create_sign_change_entry_date),
            Button(Const("Изменить Время"), id="change_time", on_click=to_create_sign_entry_time)
        ),
        Button(Const("Сохранить запись"), id="save_sign", on_click=to_save_opensign),
        Button(Const("Вернуться в главное меню"), id="back_main_menu", on_click=to_main_menu),
        state=Master_Create_Sign.confim_entries
    )

]
###===============Dialog======================###
master_dialog = Dialog(*master_main_menu)
master_create_sign_dialog = Dialog(*create_sign)