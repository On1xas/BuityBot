import datetime
import time

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction, AsyncConnection
from sqlalchemy import insert, select, update, delete, ScalarResult


from database.models import *

class Db:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    def _date_to_str(self, date: datetime.date) -> str:
        return datetime.datetime.strftime(date, '%d.%m.%Y')

    def _date_str_to_date(self, date: str) -> datetime.date:
        return datetime.datetime.strptime(date, '%d.%m.%Y')

    def _time_str_to_time(self, t: str) -> datetime.time:
        return datetime.datetime.strptime(t, '%H:%M')

    def _time_time_to_str(self, t: datetime.time):
        return datetime.time.strftime(t, '%H:%M')


class Master(Db):
    def __init__(self, session):
        super().__init__(session)

    async def set_open_sign(self, master_id: int, date: str, times: list) -> None:
        for time in times:
            query = insert(OpenSign).values(master_id=master_id, date=date,time=self._time_str_to_time(time))
            result = await self.session.execute(query)
            print(result)

    async def get_open_sign(self, date: datetime.date = None) -> dict:
        answer = {}
        if date is None:
            query = select(OpenSign).order_by(OpenSign.date)
        else:
            query = select(OpenSign).where(date==date).order_by(OpenSign.date)
        result: ScalarResult = await self.session.execute(query)
        for row in result.all():
            r : OpenSign = row[0]
            answer[r.master_id]=answer.get(r.master_id, {})
            answer[r.master_id][self._date_to_str(r.date)]=answer[r.master_id].get(self._date_to_str(r.date),[])
            answer[r.master_id][self._date_to_str(r.date)].append(self._time_time_to_str(r.time))
        print("Answer", answer)
        return answer
