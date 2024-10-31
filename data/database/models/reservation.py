from peewee import ForeignKeyField, TimeField

from data.database.models.work_slot import WorkSlotDB
from data.database.database import BaseDatabaseModel
from data.database.models.route import RouteDB
from data.database.models.user import UserDB


class ReservationDB(BaseDatabaseModel):
    user = ForeignKeyField(UserDB, backref="reservations")
    route = ForeignKeyField(RouteDB)
    start = TimeField()
    slot = ForeignKeyField(WorkSlotDB, backref="reservations")

    class Meta:
        table_name = "reservations"
