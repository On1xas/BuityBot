import sqlite3

from aiogram.types import Message


async def start_sqlite():
    global connect, cursor
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()
    print("DB connected")
    # Таблица запланированных записей
    cursor.execute("""CREATE TABLE IF NOT EXISTS planed_sings(
                    id INTEGER PRIMARY KEY, data DATE,
                    time TIME, category TEXT, client_id INT,
                     client_nickname TEXT,
                    client_name TEXT, phone TEXT, status_sing TEXT)""")
    # Таблица перечня категорий
    cursor.execute("""CREATE TABLE IF NOT EXISTS category(
                    id INTEGER PRIMARY KEY, category_name TEXT, duration TIME)
                    """)
    # Таблица доступных свободных записей
    cursor.execute("""CREATE TABLE IF NOT EXISTS work_time(
                    id INTEGER PRIMARY KEY,
                     date DATE, time TIME)""")
    # Таблица всех пользователей которые записывались
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY,
                    user_nickname TEXT, user_name TEXT, phone TEXT,
                    invite_date DATETIME, last_update DATETIME)""")
    # Блэклист пользователей
    cursor.execute("""CREATE TABLE IF NOT EXISTS blacklist_user(user_id INT,
                    description TEXT)""")
    connect.commit()


async def create_table_user_history(message: Message):
    # Таблица истории заказов пользователя
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS user_{message.from_user.id}
                    (date DATE, time TIME, category TEXT)""")
    connect.commit()