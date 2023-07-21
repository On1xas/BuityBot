from datetime import date

from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row, Multiselect, Calendar, Column
from aiogram_dialog.widgets.text import Const, Format
from aiogram.types import Message, CallbackQuery


from FSM.master_state import Master_Create_Sign, Master_Menu
from services.db_service import Master
###===============Handlers======================###
async def master_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Master_Menu.main, show_mode=StartMode.RESET_STACK)


###===============Clikers======================###
async def to_create_sign_entry_date(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.done()
    await manager.start(state=Master_Create_Sign.entry_date)


async def on_date_selected(callback: CallbackQuery, widget,
                           manager: DialogManager, selected_date: date):
    await callback.answer(str(selected_date))
    print(manager.middleware_data)
    print(date.today())
    await manager.switch_to(Master_Create_Sign.menu_templates)

###===============Getters======================###


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
    state=Master_Create_Sign.entry_date),
    Window(
        Const("Выберите время"),
        Row(
            Button(Const("Создать шаблон"), id="create_template"),
            Button(Const("Изменить шаблон"), id="edit_template"),
            Button(Const("Удалить шаблон"), id="delete_template")
        ),
        Button(Const("Тут Будет Multiselect из времени основного шаблона"), id="tempid"),
        Column(
            Button(Const("Шаблон 1"),id="template_1"),
            Button(Const("Шаблон 2"),id="template_2"),
        ),
        Button(Const("Вернуться в главное меню"), id="back_main_menu"),
        state=Master_Create_Sign.menu_templates
)
]
###===============Dialog======================###
master_dialog = Dialog(master_main_menu)
master_create_sign_dialog = Dialog(*create_sign)