import io
from typing import Optional

import peewee

from data.database.models.file import FileDB


class FileDataSource:
    @staticmethod
    def create_file(_bytes: bytes) -> int:
        file = FileDB(content=io.BytesIO(_bytes).getvalue())
        file.save()
        return file.id

    @staticmethod
    def get_file(_id: int) -> Optional[FileDB]:
        try:
            return FileDB.get(FileDB.id == _id)
        except peewee.DoesNotExist:
            return None
