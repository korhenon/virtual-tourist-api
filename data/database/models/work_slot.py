from peewee import ForeignKeyField, TimeField, DateField

from data.database.models.author import AuthorDB
from data.database.database import BaseDatabaseModel


class WorkSlotDB(BaseDatabaseModel):
    author = ForeignKeyField(AuthorDB, backref="work_slots")
    date = DateField()
    start = TimeField()
    end = TimeField()

    class Meta:
        table_name = "work_slots"
