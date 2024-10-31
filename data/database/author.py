from typing import Optional

import peewee

from data.database import UserDB, AuthorDB


class AuthorDataSource:
    @staticmethod
    def create_author(user: UserDB, name: str) -> bool:
        try:
            AuthorDB(user=user, name=name, description="").save()
            return True
        except peewee.IntegrityError:
            return False

    @staticmethod
    def get_author_by_user(user: UserDB) -> Optional[AuthorDB]:
        try:
            return AuthorDB.get((AuthorDB.user == user))
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def get_author_by_id(_id: int) -> Optional[AuthorDB]:
        try:
            return AuthorDB.get((AuthorDB.id == _id))
        except peewee.DoesNotExist:
            return None

