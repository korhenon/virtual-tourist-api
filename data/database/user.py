from typing import Optional

import peewee

from data.database import UserDB


class UserDataSource:
    @staticmethod
    def create_user(name: str, email: str, password: str) -> bool:
        try:
            UserDB(name=name, email=email, password=password).save()
            return True
        except peewee.IntegrityError:
            return False

    @staticmethod
    def get_user_by_email(email: str) -> Optional[UserDB]:
        try:
            return UserDB.get(UserDB.email == email)
        except peewee.DoesNotExist:
            return None
