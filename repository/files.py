from data.files import FilesDataSource


class FilesRepository:
    def __init__(self, datasource: FilesDataSource):
        self.ds = datasource

    def get_privacy(self):
        return self.ds.privacy_file


