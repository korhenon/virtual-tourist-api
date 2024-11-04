import os


class EnvironmentDataSource:

    @staticmethod
    def get_jwt_secret() -> str:
        return os.environ.get("JWT_SECRET")

    @staticmethod
    def get_pg_host() -> str:
        return os.environ.get("PG_HOST")

    @staticmethod
    def get_pg_database() -> str:
        return os.environ.get("PG_DATABASE")

    @staticmethod
    def get_pg_user() -> str:
        return os.environ.get("PG_USER")

    @staticmethod
    def get_pg_password() -> str:
        return os.environ.get("PG_PASSWORD")
