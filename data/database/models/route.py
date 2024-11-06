from peewee import ForeignKeyField, TextField, IntegerField, FloatField

from data.database.models.author import AuthorDB
from data.database.database import BaseDatabaseModel
from data.database.models.file import FileDB


class RouteDB(BaseDatabaseModel):
    author = ForeignKeyField(AuthorDB, backref="routes")
    name = TextField()
    price = IntegerField()
    time = IntegerField()
    description = TextField()
    start_latitude = FloatField()
    start_longitude = FloatField()
    photo = ForeignKeyField(FileDB)

    class Meta:
        table_name = "routes"
