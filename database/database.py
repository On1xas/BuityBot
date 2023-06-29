import asyncpg
from aiogram.types import Message


class RequestDB:
    def __init__(self, connect_pool: asyncpg.pool.Pool):
        self.pool = connect_pool

    async def add_sign(self, date, time):
        query = """
        """





# async def start_sqlite():
#     global connect, cursor
#     connect = sqlite3.connect("database.db")
#     cursor = connect.cursor()
#     print("DB connected")
#     # Таблица запланированных записей
#     cursor.execute("""CREATE TABLE IF NOT EXISTS planed_sings(
#                     id INTEGER PRIMARY KEY, data DATE,
#                     time TIME, category TEXT, client_id INT,
#                      client_nickname TEXT,
#                     client_name TEXT, phone TEXT, status_sing TEXT)""")
#     # Таблица перечня категорий
#     cursor.execute("""CREATE TABLE IF NOT EXISTS category(
#                     id INTEGER PRIMARY KEY, category_name TEXT, duration TIME)
#                     """)
#     # Таблица доступных свободных записей
#     cursor.execute("""CREATE TABLE IF NOT EXISTS work_time(
#                     id INTEGER PRIMARY KEY,
#                      date DATE, time TIME)""")
#     # Таблица всех пользователей которые записывались
#     cursor.execute("""CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY,
#                     user_nickname TEXT, user_name TEXT, phone TEXT,
#                     invite_date DATETIME, last_update DATETIME)""")
#     # Блэклист пользователей
#     cursor.execute("""CREATE TABLE IF NOT EXISTS blacklist_user(user_id INT,
#                     description TEXT)""")
#     connect.commit()


# async def create_table_user_history(message: Message):
#     # Таблица истории заказов пользователя
#     cursor.execute(f"""CREATE TABLE IF NOT EXISTS user_{message.from_user.id}
#                     (date DATE, time TIME, category TEXT)""")
#     connect.commit()

###-------------------------------------------------------------------------------
#Таблица созданных записей
query = """CREATE TABLE IF NOT EXISTS open_sign (
id serial PRIMARY KEY,
date DATE,
time TIME)"""

#Добавление записи в таблицу созданных записей
query = """CREATE TABLE IF NOT EXISTS open_sign (
id serial PRIMARY KEY,
date DATE,
time TIME)"""

#Таблица записанных юзеров
query = """CREATE TABLE IF NOT EXISTS sign (
id_sign serial PRIMARY KEY,
date DATE,
time TIME,
user_id INT,
username_ru VARCHAR(25),
phone VARCHAR(13),
service VARCHAR(150))"""




###-------------------------------------------------------------------------------
#Таблица мастеров
query = """CREATE TABLE IF NOT EXISTS master_users (
user_id SERIAL PRIMARY KEY,
username VARCHAR(25),
first_name VARCHAR(25),
last_name VARCHAR(25))"""

#Таблица шаблона мастера
query = """CREATE TABLE IF NOT EXISTS master_{master_id}_templates_sign (
id_template SERIAL PRIMARY KEY,
name_template VARCHAR(50),
table_name_value VARCHAR(50)
)"""

#Таблица значений шаблона мастера
query = """CREATE TABLE IF NOT EXISTS value_template_{master_id}_sign (
id_template SERIAL PRIMARY KEY REFERENCES master_{master_id}_templates_sign (id_template),
value VARCHAR(5)
)"""


import asyncpg
import asyncio
import datetime

time='11:00'
async def start():
    connect = await asyncpg.connect(user="topevgn", password="1234", host="localhost", database="bot")
    print(connect)
    query = """INSERT INTO open_sign (datetime, times) VALUES ($1, $2)"""

    date='23/01/2023'
    time='11:00'
    print()
    print()
    await connect.execute(query, datetime.datetime.strptime(date,'%d/%m/%Y').date(), datetime.datetime.strptime(time,'%H:%M').time())

    await connect.close()


if __name__ == "__main__":
    print(datetime.datetime.strptime(time,'%H:%M'))
    asyncio.run(start())