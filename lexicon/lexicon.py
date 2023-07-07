

LEXICON_RU: dict[str, str] = {
    "start": "Приветсвуем вас! Тут вы можете быстро самостоятельно произвести запись",
    "sing": """Инструкция о процессе записи:\n\n
            1. Переходите в меню записи нажав кнопку Выбрать дату\n
            2. Выбрав дату, переходи в меню выбора времени\n
            3. Выберите желаемую услугу.\n
            4. После обработки полученной заявки мастер с вами свяжется для подтверждения записи
            """,
    "my_sing": "Ваши записи:",
    "history_sing": "История ваших записей:",
    "portfolio": "Выберите какая услуга вас интересует",
    "price": """Прейскурант на предоставляемые услуги:\n
                1. 2 BYN
                2. 3 BYN
                3. 4 BYN""",
    "master_succes": "Вы успешно зашли в раздел мастера. \nВы берайте раздел для работы:",
    "master_denied": "Вы не мастер",
    "FSM_MasterCreateSign_date": "Выберите дату на которую хотите создать записи:",
    "FSM_MasterCreateSign_time": "Выберите время на которые хотите записи:",
    "FSM_MasterCreateSign_finish": """<b>Вы хотите создать запись для клиентов:</b>\n
\tДата: <i><u>{date}</u></i>
\tВремя: <i><u>{times}</u></i>
    """,
    "check_open_sign": """<b>Свободные записи:</b>\n"""
}

LEXICON_COMMANDS_RU: dict[str, str] = {
                '/start': 'Главное меню',
                '/sing': 'Записаться на приём',
                '/my_sing': 'Мои текущие записи',
                '/history_sing': 'История записей',
                '/portfolio': 'Портфолио',
                '/price': 'Прейскурант'
                }


LEXICON_KB_ADMIN_MAIN: dict[str, str] = {
    "create_sign" : "Создать запись",
    "edit_sign" : "Изменить запись",
    "check_sign" : "Проверить записи",
    "delete_sign" : "Удалить запись"
}

LEXICON_KB_ADMIN_FSM_CreateSign_edit: dict[str, str] = {
    "edit_date": "Изменить дату",
    "edit_time": "Изменить время",
    "save": "Создать запись"
}
LEXICON_TIME_CONST: dict[str, list[str]] = {
    "standart_time": ["11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]
}

LEXICON_RU_BUTTON: dict[str, str] = {
    "create_template": "Создать шаблон",
    "use_template": "Использовать шаблон",
    "back_main_menu": "Вернуться в главное меню",
    "back_time_menu": "Вернуться в меню выбора времени",
    "time_selected": "Выбрать время",
    "edit_main_template": "Изменить шаблон по умолчанию"
}
LEXICON_RU_MULTI_SELECT_BUTTON = {
    "times_to_sign": ["11:00", "12:00", "13:00", "14:00"]
}
LEXICON_RU_MASTER_TEMPLATE_BUTTON: dict[str, str] = {
    "create_template": "Создать шаблон",
    "edit_template": "Изменить шаблон",
    "delete_template": "Удалить шаблон"
}