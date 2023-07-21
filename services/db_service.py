import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete


from database.models import *

class Db:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    def _date_to_str(self, date: datetime.date) -> str:
        return datetime.datetime.strftime(date, '%d.%m.%Y')

    def _date_str_to_date(self, date: str) -> datetime.date:
        return datetime.datetime.strptime(date, '%d.%m.%Y')



class Master(Db):
    def __init__(self, session):
        super.__init__(session)

    def set_open_sign(self, date: str, times: list) -> None:
        for time in times:
            query = insert(OpenSign).values(date=self._date_str_to_date(date),time=time)
            result = self.session.execute(query)
            print(result)