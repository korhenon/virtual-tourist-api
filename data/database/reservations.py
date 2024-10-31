import datetime

from data.database import WorkSlotDB, ReservationDB, UserDB, RouteDB


class ReservationsDataSource:
    @staticmethod
    def get_by_slot(slot: WorkSlotDB) -> list[ReservationDB]:
        return list(slot.reservations.order_by(ReservationDB.start))

    @staticmethod
    def create(user: UserDB, route: RouteDB, start: datetime.time, slot: WorkSlotDB):
        ReservationDB(user=user, route=route, start=start, slot=slot).save()
