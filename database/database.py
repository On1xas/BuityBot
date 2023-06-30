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
user_id INT PRIMARY KEY,
username VARCHAR(25),
first_name VARCHAR(25),
last_name VARCHAR(25))"""

#Таблица шаблона мастера
query = """CREATE TABLE IF NOT EXISTS master_templates_sign (
id_template SERIAL PRIMARY KEY,
user_id INT NOT NULL,
name_template VARCHAR(50),
is_main_template BOOL DEFAULT False,
callback_key VARCHAR(25),
time_template VARCHAR(5) ARRAY
)"""
## Добавление шаблона мастера
query = """INSERT INTO master_templates_sign (user_id, name_template, callback_key, time_template) VALUES ($1, $2, $3, $4)"""
### Callback_key генерируется -> "edit_template" + id_template
###-------------------------------------------------------------------------------



import asyncpg
import asyncio
import datetime

time='11:00'
async def start():
    connect = await asyncpg.connect(user="topevgn", password="1234", host="localhost", database="bot")
    print(connect)
    query = """INSERT INTO master_templates_sign (user_id, name_template, callback_key, time_template) VALUES ($1, $2, $3, $4)"""

    date='23/01/2023'
    time='11:00'
    id=20253994
    print()
    print()
    await connect.execute(query, id, "Not main", 'edit_template_', ['11:00', '12:00'])

    await connect.close()


if __name__ == "__main__":
    print(datetime.datetime.strptime(time,'%H:%M'))
    asyncio.run(start())