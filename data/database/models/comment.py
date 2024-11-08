from peewee import ForeignKeyField, IntegerField, TextField

from data.database.models.route import RouteDB
from data.database.models.user import UserDB
from data.database.database import BaseDatabaseModel


class CommentDB(BaseDatabaseModel):
    user = ForeignKeyField(UserDB, backref="comments")
    route = ForeignKeyField(RouteDB, backref="comments")
    mark = IntegerField()
    text = TextField()

    class Meta:
        table_name = "comments"
