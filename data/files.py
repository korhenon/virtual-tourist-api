from datetime import datetime
import os.path
from typing import Optional


class FilesDataSource:
    media_folder = ".files/media"
    privacy_file = ".files/privacy.pdf"

    def save_image(self, unique_name: str, _bytes: bytes) -> str:
        if not os.path.exists(self.media_folder):
            os.mkdir(self.media_folder)

        now = str(datetime.now()).replace(' ', '_').replace('.', '_').replace(':', '_').replace('-', '_')
        filename = unique_name + now + ".png"

        with open(self.media_folder + "/" + filename, "wb") as file:
            file.write(_bytes)
        return filename

    def get_file(self, filename: str) -> Optional[str]:
        path = self.media_folder + "/" + filename
        if os.path.exists(path):
            return path
        return None
