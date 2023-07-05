import datetime
from copy import deepcopy
import asyncpg
from aiogram.fsm.context import FSMContext

class RequestDB:
    def __init__(self, connection: asyncpg.pool.Pool):
        self.connect = connection

    async def set_opensign(self, date: str, times: list):
        query = """INSERT INTO open_sign (date, time) VALUES ($1, $2)"""

        # Запрос данных для проверки на задвоения
        base = await self.get_opensign()
        # Проверяем есть ли такая дата уже есть в базе
        filter_list = []
        if date in base:
            # Если дата в базе уже есть, проверяем по списку временных совпадения с уже созданными датами
            for time in times:
                # Проверяем есть ли время в списке временных по выбранному дню
                if time not in base[date]:
                    # Если время не задвоено0 добавляем его в список
                    filter_list.append(time)
        else:
            filter_list = deepcopy(times)
        # Подготовка параметра класса Дататайм для добавления в табилцу
        date = datetime.datetime.strptime(date, '%d.%m.%Y')
        # В цикле добавляем записи
        for time in filter_list:
            # Подготовка параметра класса Дататайм для добавления в табилцу
            time_class = datetime.datetime.strptime(time, '%H:%M')
            await self.connect.execute(query, date, time_class)

#
    async def get_opensign(self, value: str=None) -> dict[str,list]:
        """
        send date in parametr - value: str in format  %d.%m.%Y
        """
        if value is None:
            query = """SELECT (date, time, id) FROM open_sign"""
                    # Получаем ответ класса Records
            result = await self.connect.fetch(query)
        else:

            query = """SELECT (date, time, id) FROM open_sign WHERE date = $1"""
            # Получаем ответ класса Records
            value=datetime.datetime.strptime(value, '%d.%m.%Y')
            result = await self.connect.fetch(query, value)

        date_now=datetime.datetime.now()
        # Словарь для ответа
        answer: dict[str, list] = {}
        # Распаковываем список строк
        for res in result:
            # Распаковываем кортеж с значениями в строках методом values()
            for row in res.values():
                # Формируем переменную класса Datetime для сравнения
                check_day = datetime.datetime(year=row[0].year, month=row[0].month, day=row[0].day, hour=row[1].hour, minute=row[1].minute)
                # Проверяем актуальные ли данные в строке
                if date_now <= check_day:
                    # Проверяем имеется ли ключ с датой в ответе
                    if check_day.strftime('%d.%m.%Y') in answer:
                        # то добавляем время в значения ключа
                        answer[check_day.strftime('%d.%m.%Y')].append(check_day.strftime('%H:%M'))
                    # Создаем ключ
                    answer[check_day.strftime('%d.%m.%Y')]=answer.get(check_day.strftime('%d.%m.%Y'), [check_day.strftime('%H:%M')])
                else:
                    # Если данные не актуальные удаляем их из таблицы.
                    drop_query = """DELETE FROM open_sign WHERE id=$1"""
                    await self.connect.execute(drop_query, row[2])
        return answer

    async def update_opensign(self, date_update: str, old_time: str, new_time: str) -> bool:                   #### ДОБАВИТЬ ПРОВЕРКУ НА ЗАДВОЕНИЕ
        '''GET:
                    date_update: str in format %d.%m.%Y
                    old_time: str in format %H:%M
                    new_time: str in format %H:%M

                return status update:
                    True - Good
                    False -Dublicate new_time in open_sign table or Exceptions'''

        date = datetime.datetime.strptime(date_update, '%d.%m.%Y')
        old_time = datetime.datetime.strptime(old_time, '%H:%M')
        new_t = datetime.datetime.strptime(new_time, '%H:%M')

        query = """UPDATE open_sign SET time = $3 WHERE date = $1 and time = $2"""
        actual_time = await self.get_opensign(date_update)
        if new_time not in actual_time[date_update]:
            await self.connect.execute(query, date, old_time, new_t)
            return True
        return False


    async def delete_opensign(self, date: str, time: str):

        query = """DELETE FROM open_sign WHERE date = $1 AND time = $2"""
        
        date = datetime.datetime.strptime(date, '%d.%m.%Y')
        time = datetime.datetime.strptime(time, '%H:%M')

        await self.connect.execute(query, date, time)

    async def create_template_opensign(self):
        pass

    async def update_template_opensign(self):
        pass

    async def get_template_opensign(self, master_user_id: int):
        
        query = """SELECT * FROM master_templates_sign WHERE user_id = $1"""

        result = await self.connect.fetch(query, master_user_id)
        answer = {}
        keys = ["id", "is_main", "callback_key", "times"]
        for res in result:
            row = (tuple(res))
            answer[row[2]] = answer.get(row[2],(dict(zip(keys, (row[0], row[3], row[4]+str(row[0]), row[5])))))

        return answer

    async def delete_template_opensign():
        pass


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

# Таблица созданных записей
query = """CREATE TABLE IF NOT EXISTS open_sign (
id serial PRIMARY KEY,
date DATE,
time TIME)"""

# get_opensign Запрос на выборку всех пустых записей начиная с TODAY и TIMENOW
query = """SELECT (datetime, times, id) FROM open_sign"""

# set_opensign Вставка открытых записей в таблицу.
query = """INSERT INTO open_sign (date, time) VALUES ($1, $2)"""

#Таблица записанных юзеров
query = """CREATE TABLE IF NOT EXISTS sign (
id_sign serial PRIMARY KEY,
date DATE,
time TIME,
user_id INT,
username_ru VARCHAR(25),
phone VARCHAR(13),
service VARCHAR(150))"""

# Всенение изменения в записи
query = """UPDATE open_sign SET time = '$3 WHERE date = $1 and time = $2"""

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

## Добавление шаблона мастера. Callback_key генерируется -> "edit_template_" + id_template
query = """INSERT INTO master_templates_sign (user_id, name_template, callback_key, time_template) VALUES ($1, $2, $3, $4)"""
###
###-------------------------------------------------------------------------------



import asyncpg
import asyncio
import datetime

time='11:00'

async def start():
    connect: asyncpg.connect = await asyncpg.connect(user="topevgn", password="1234", host="localhost", database="bot")
    # date_update = datetime.datetime.strptime(date_update, '%d.%m.%Y')
    # old_time = datetime.datetime.strptime(old_time, '%H:%M')
    # new_time = datetime.datetime.strptime(new_time, '%H:%M') 
    # query = """UPDATE open_sign SET time = $3 WHERE date = $1 and time = $2"""
    # await connect.execute(query, date_update, old_time, new_time)

    db=RequestDB(connection=connect)
    print(await db.get_template_opensign(master_user_id=20253994))


if __name__ == "__main__":
    asyncio.run(start())