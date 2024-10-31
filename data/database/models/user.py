from peewee import TextField

from data.database.database import BaseDatabaseModel


class UserDB(BaseDatabaseModel):
    name = TextField()
    email = TextField(unique=True)
    password = TextField()
    photo = TextField(null=True, default=None)

    class Meta:
        table_name = "users"
