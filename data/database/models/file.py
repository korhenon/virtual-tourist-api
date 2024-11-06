from peewee import BlobField

from data.database.database import BaseDatabaseModel


class FileDB(BaseDatabaseModel):
    content = BlobField()

    class Meta:
        table_name = "files"
