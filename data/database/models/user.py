from peewee import TextField, ForeignKeyField

from data.database.database import BaseDatabaseModel
from data.database.models.file import FileDB


class UserDB(BaseDatabaseModel):
    name = TextField()
    email = TextField(unique=True)
    password = TextField()
    photo = ForeignKeyField(FileDB, null=True, default=None)

    class Meta:
        table_name = "users"
