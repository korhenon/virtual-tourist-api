from common import sha256
from data.database.file import FileDataSource
from repository.auth import AuthRepository


class FileNotFound(Exception):
    pass


class FilesRepository:
    def __init__(self, datasource: FileDataSource, auth_repository: AuthRepository):
        self.ds = datasource
        self.ar = auth_repository

    def upload_photo(self, token: str, _bytes: bytes) -> int:
        self.ar.authorize(token)
        return self.ds.create_file(_bytes)

    def get_file(self, file: int) -> bytes:
        path = self.ds.get_file(file)
        if path is None:
            raise FileNotFound
        return path
