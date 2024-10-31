import os


class EnvironmentDataSource:
    @staticmethod
    def get_jwt_secret() -> str:
        return os.environ.get("JWT_SECRET")
