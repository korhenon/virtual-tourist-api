import datetime

from peewee import Model, PrimaryKeyField, DateTimeField, PostgresqlDatabase

from data import setup_environment
from data.environment import EnvironmentDataSource

setup_environment()
db = PostgresqlDatabase(
    database=EnvironmentDataSource.get_pg_database(),
    user=EnvironmentDataSource.get_pg_user(),
    password=EnvironmentDataSource.get_pg_password(),
    host=EnvironmentDataSource.get_pg_host()
)


class BaseDatabaseModel(Model):
    id = PrimaryKeyField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
