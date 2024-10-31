import datetime

from peewee import SqliteDatabase, Model, PrimaryKeyField, DateTimeField

db = SqliteDatabase("database.db")


class BaseDatabaseModel(Model):
    id = PrimaryKeyField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
