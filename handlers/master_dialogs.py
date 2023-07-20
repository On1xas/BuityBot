from datetime import date

from aiogram_dialog import Dialog, DialogManager, StartMode, Window, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Multiselect, Calendar, Column
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import Message, CallbackQuery, ContentType


from FSM.master_state import Master_Create_Sign, Master_Menu

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
        dialog_manager.dialog_data.get("times", message.text.split(","))
        await dialog_manager.switch_to(Master_Create_Sign.confim_entries)
        dialog_manager.dialog_data["status_state"] = "confim"
    else:
        await message.answer("Ввел хуйню")

###===============Clikers======================###
async def to_create_sign_entry_date(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.done()
    await manager.start(state=Master_Create_Sign.entry_date, mode=StartMode.NORMAL)
    print(manager.middleware_data)

async def to_create_sign_entry_time(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(state=Master_Create_Sign.entry_time)


async def on_date_selected(callback: CallbackQuery, widget,
                           manager: DialogManager, selected_date: date):

    if selected_date < date.today():
        await callback.answer(text=f"{str(selected_date)} - уже прошла, выберите актуальную")
    else:
        if manager.dialog_data["status_state"] == "confim":
            manager.dialog_data["date"]=selected_date
            await manager.switch_to(Master_Create_Sign.confim_entries)
        else:
            manager.dialog_data["date"]=selected_date
            await manager.switch_to(Master_Create_Sign.menu_templates)

###===============Getters======================###
async def get_data(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data.get("date", date.today())
    dialog_manager.dialog_data.get("status_state", None)
    print(dialog_manager.dialog_data)
    return dialog_manager.dialog_data

###===============When======================###


###===============Windows======================###
master_main_menu = Window(
    Const("Вы находите в 🎈 главном меню мастера:"),
    Row(
        Button(Const("Создать запись"), id="create_sign", on_click=to_create_sign_entry_date),
        Button(Const("Изменить запись"), id="edit_sign")
    ),
    Row(
        Button(Const("Проверить запись"), id="check_sign"),
        Button(Const("Удалить запись"), id="delete_sign")
    ),
    state=Master_Menu.main
    )

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
        Button(Const("Вернуться в главное меню"), id="back_main_menu"),
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
            Button(Const("Изменить Дату"), id="change_date", on_click=to_create_sign_entry_date),
            Button(Const("Изменить Время"), id="change_date", on_click=to_create_sign_entry_time)
        ),
        Button(Const("Сохранить запись"), id="save_sign"),
        Button(Const("Вернуться в главное меню"), id="back_main_menu"),
        state=Master_Create_Sign.confim_entries
    )

]
###===============Dialog======================###
master_dialog = Dialog(master_main_menu)
master_create_sign_dialog = Dialog(*create_sign)