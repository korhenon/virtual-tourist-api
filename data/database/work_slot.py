import datetime
from typing import Optional

import peewee

from data.database import AuthorDB, WorkSlotDB


class WorkSlotDataSource:
    @staticmethod
    def get_by_id(_id) -> Optional[WorkSlotDB]:
        try:
            return WorkSlotDB.get(id=_id)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def get_upcoming(author: AuthorDB) -> list[WorkSlotDB]:
        date = datetime.date.today()
        query = WorkSlotDB.select().where((WorkSlotDB.author == author) & (WorkSlotDB.date >= date)).order_by(WorkSlotDB.date)
        return list(query)

    @staticmethod
    def create(author: AuthorDB, date: datetime.date, start: datetime.time, end: datetime.time):
        WorkSlotDB(author=author, date=date, start=start, end=end).save()

    @staticmethod
    def update(slot: WorkSlotDB, start: datetime.time, end: datetime.time):
        slot.start = start
        slot.end = end
        slot.save()

    @staticmethod
    def delete(slot: WorkSlotDB):
        slot.delete_instance()

    @staticmethod
    def get_booked_dates(author: AuthorDB) -> list[datetime.date]:
        date = datetime.date.today()
        query = WorkSlotDB.select().where((WorkSlotDB.author == author) & (WorkSlotDB.date > date)).order_by(WorkSlotDB.date)
        booked_dates = []
        for i in query:
            booked_dates.append(i.date)
        return booked_dates
