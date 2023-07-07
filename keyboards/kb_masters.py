import datetime

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext


from lexicon.lexicon import (LEXICON_KB_ADMIN_MAIN,
                             LEXICON_RU_BUTTON,
                             LEXICON_KB_ADMIN_FSM_CreateSign_edit,
                             LEXICON_TIME_CONST,
                             LEXICON_RU_MULTI_SELECT_BUTTON,
                             LEXICON_RU_MASTER_TEMPLATE_BUTTON)
from database.database import RequestDB



def kb_master_back_main_menu():
    kb = InlineKeyboardBuilder()
    kb.row(*button_back_main_menu())
    return kb.as_markup()

# Главное меню для Мастер юзера
def create_kb_master_main():
    kb_admin_main = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON_KB_ADMIN_MAIN.items()]
    kb_admin_main.row(*buttons, width=2)
    return kb_admin_main.as_markup()


def button_back_main_menu():
    return [InlineKeyboardButton(text=LEXICON_RU_BUTTON["back_main_menu"], callback_data="back_main_menu")]


def create_kb_fsm_CreateSign_time():
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=value) for value in LEXICON_TIME_CONST['standart_time']]
    buttons.append(InlineKeyboardButton(text=LEXICON_RU_BUTTON["create_template_time"], callback_data="create_template_time"))
    kb.row(*buttons, width=5)
    kb.row(*button_back_main_menu())
    return kb.as_markup()


def create_kb_fsm_CreateSign_edit():
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON_KB_ADMIN_FSM_CreateSign_edit.items()]
    kb.row(*buttons, width=2)
    kb.row(*button_back_main_menu())
    return kb.as_markup()


async def kb_multiselect_master_sign(state: FSMContext, database: RequestDB):
    kb = InlineKeyboardBuilder()
    selected = await state.get_data()
    main_button = []

    for time in LEXICON_RU_MULTI_SELECT_BUTTON['times_to_sign']:
        if selected and time in selected['times']:
            main_button.append(InlineKeyboardButton(text=f"[{time}]",
                               callback_data=time))
        else:
            main_button.append(InlineKeyboardButton(text=f"{time}",
                               callback_data=time))
    kb.row(*main_button, width=5)
    kb.row(InlineKeyboardButton(text=LEXICON_RU_BUTTON["time_selected"],
                                callback_data="time_selected"), width=1)
    return kb.as_markup()

async def kb_select_master_edit_opensign(state: FSMContext, database: RequestDB):
    kb = InlineKeyboardBuilder()
    selected = await state.get_data()
    db_open_sign = await database.get_opensign(value=selected['date'])
    main_button = []
    for time in sorted(db_open_sign[selected['date']]):
            main_button.append(InlineKeyboardButton(text=f"Изменить запись {selected['date']} - {time}",
                                callback_data=time))
    kb.row(*main_button, width=1)
    kb.row(*button_back_main_menu())
    return kb.as_markup()

async def kb_multiselect_delete_master_sign(state: FSMContext, database: RequestDB):
    kb = InlineKeyboardBuilder()
    selected = await state.get_data()
    main_button = []
    db_open_sign = await database.get_opensign(value=selected['date'])
    for time in sorted(db_open_sign[selected['date']]):
        if selected and time in selected['times']:
            main_button.append(InlineKeyboardButton(text=f"Удалить запись [{time}]",
                                callback_data=time))
        else:
            main_button.append(InlineKeyboardButton(text=f"Удалить запись  {time}",
                                callback_data=time))
    kb.row(*main_button, width=1)
    kb.row(InlineKeyboardButton(text=LEXICON_RU_BUTTON["time_selected"],
                                    callback_data="time_selected"), width=1)
    return kb.as_markup()



async def kb_multiselect_start_create_opensign(state: FSMContext):

    kb = InlineKeyboardBuilder()

    selected = await state.get_data()
    print(selected)
    main_button = []
    #Кнопка использовать шаблоны
    kb.row(*[InlineKeyboardButton(text=LEXICON_RU_BUTTON["use_template"], callback_data='use_template')])
    #Кнопки из стандартного шаблона
    if selected['main_template']:
        for time in sorted(selected['main_template']['times']):
            if selected and time in selected['select_times']:
                main_button.append(InlineKeyboardButton(text=f"[{time}]",
                                    callback_data=time))
            else:
                main_button.append(InlineKeyboardButton(text=f"{time}",
                                    callback_data=time))
        kb.row(*main_button, width=8)
    # Кнопка выбрать время
    kb.row(InlineKeyboardButton(text=LEXICON_RU_BUTTON["time_selected"],
                                    callback_data="time_selected"), width=1)
    #Кнопка Ввести время самому
    kb.row(*[InlineKeyboardButton(text="Ввести время вручную", callback_data='entry_manually')])

    # Кнопка выйти в главное меню
    kb.row(*button_back_main_menu())

    return kb.as_markup()


async def kb_multiselect_templates_create_opensign(templates: dict):
    kb = InlineKeyboardBuilder()
    #3 Кнопки - Создать шаблон, Удалить шаблон, Изменить шаблон
    menu_button = [InlineKeyboardButton(text=LEXICON_RU_MASTER_TEMPLATE_BUTTON[key], callback_data=key) for key in LEXICON_RU_MASTER_TEMPLATE_BUTTON]
    kb.row(*menu_button, width=3)
    #Изменить шаблон по умолчанию
    kb.row(InlineKeyboardButton(text=LEXICON_RU_BUTTON['edit_main_template'], callback_data="edit_main_template"), width=1)
    templates_button = []
    #Кнопки - перечень созданных шаблонов
    for key in templates:
        if not templates[key]['is_main']:
            text = key + "  -  " + ",".join(sorted(templates[key]["times"]))
            templates_button.append(InlineKeyboardButton(text=text, callback_data=templates[key]["callback_key"]))
    kb.row(*templates_button, width=1)
    #Кнопка вернуся в Мультиселект
    kb.row(InlineKeyboardButton(text=LEXICON_RU_BUTTON["back_time_menu"], callback_data="back_time_menu"), width=1)
    #Кнопка вернуть в главное меню
    kb.row(*button_back_main_menu())

    return kb.as_markup()

async def kb_multiselect_create_templates_create_opensign():
    # ЗАПРОС НА ВВЕДЕНИЕ ШАБЛОНА текстом
    #Кнопка вернуся в меню шаблонов
    #Кнопка вернуть в главное меню
    pass
async def kb_multiselect_delete_templates_create_opensign():
    # Кнопки существиющих шаблонов
    #Кнопка вернуся в меню шаблонов
    #Кнопка вернуть в главное меню
    pass
async def kb_multiselect_delete_check_templates_create_opensign():
    # Кнопки Да, Нет - подстверждение удаления шаблона
    #Кнопка вернуся в меню шаблонов
    #Кнопка вернуть в главное меню
    pass
async def kb_multiselect_edit_templates_create_opensign():
    # Кнопки существиющих шаблонов
    #Кнопка вернуся в меню шаблонов
    #Кнопка вернуть в главное меню
    pass
async def kb_multiselect_edit_entrynew_templates_create_opensign():
    # ЗАПРОС НА ВВЕДЕНИЕ ШАБЛОНА текстом
    #Кнопка вернуся в меню шаблонов
    #Кнопка вернуть в главное меню
    pass
async def kb_multiselect_edit_check_templates_create_opensign():
    # Кнопки Да, Нет - подстверждение изменения шаблона
    #Кнопка вернуся в меню шаблонов
    #Кнопка вернуть в главное меню
    pass

async def kb_multiselect_editmain_templates_create_opensign():
    # Кнопки существиющих шаблонов
    #Кнопка вернуся в меню шаблонов
    #Кнопка вернуть в главное меню
    pass

async def kb_multiselect_editmain_check_templates_create_opensign():
    # Кнопки Да, Нет - подстверждение изменения шаблона
    #Кнопка вернуся в меню шаблонов
    #Кнопка вернуть в главное меню
    pass