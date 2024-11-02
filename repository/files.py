from common import sha256
from data.files import FilesDataSource
from repository.auth import AuthRepository


class FileNotFound(Exception):
    pass


class FilesRepository:
    def __init__(self, datasource: FilesDataSource, auth_repository: AuthRepository):
        self.ds = datasource
        self.ar = auth_repository

    def get_privacy(self) -> str:
        return self.ds.privacy_file

    def upload_photo(self, token: str, _bytes: bytes) -> str:
        return self.ds.save_image(sha256(self.ar.authorize(token).credentials.email), _bytes)

    def get_file(self, filename) -> str:
        path = self.ds.get_file(filename)
        if path is None:
            raise FileNotFound
        return path
