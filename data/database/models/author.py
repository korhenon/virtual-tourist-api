from peewee import ForeignKeyField, TextField

from data.database.models.user import UserDB
from data.database.database import BaseDatabaseModel


class AuthorDB(BaseDatabaseModel):
    user = ForeignKeyField(UserDB, unique=True)
    name = TextField()
    description = TextField()

    class Meta:
        table_name = "authors"
