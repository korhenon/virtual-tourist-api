from peewee import ForeignKeyField

from data.database.models.user import UserDB
from data.database.models.author import AuthorDB
from data.database.database import BaseDatabaseModel


class SubscriptionDB(BaseDatabaseModel):
    user = ForeignKeyField(UserDB, backref="subscriptions")
    author = ForeignKeyField(AuthorDB, backref="subscriptions")

    class Meta:
        table_name = "subscriptions"
