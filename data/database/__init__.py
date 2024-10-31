from data.database.database import db
from data.database.models.author import AuthorDB
from data.database.models.reservation import ReservationDB
from data.database.models.route import RouteDB
from data.database.models.subscription import SubscriptionDB
from data.database.models.user import UserDB
from data.database.models.work_slot import WorkSlotDB


def setup_database():
    db.create_tables([UserDB, AuthorDB, RouteDB, SubscriptionDB, WorkSlotDB, ReservationDB])
