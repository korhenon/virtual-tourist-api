from peewee import ForeignKeyField, TextField, IntegerField, FloatField

from data.database.models.author import AuthorDB
from data.database.database import BaseDatabaseModel


class RouteDB(BaseDatabaseModel):
    author = ForeignKeyField(AuthorDB, backref="routes")
    name = TextField()
    price = IntegerField()
    time = IntegerField()
    description = TextField()
    start_latitude = FloatField()
    start_longitude = FloatField()
    photo = TextField()

    class Meta:
        table_name = "routes"
