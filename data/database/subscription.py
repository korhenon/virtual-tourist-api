import peewee

from data.database import UserDB, AuthorDB, SubscriptionDB


class SubscriptionDataSource:
    @staticmethod
    def create_subscription(user: UserDB, author: AuthorDB) -> bool:
        try:
            SubscriptionDB.get((SubscriptionDB.user == user) & (SubscriptionDB.author == author))
            return False
        except peewee.DoesNotExist:
            SubscriptionDB(user=user, author=author).save()
            return True

    @staticmethod
    def delete_subscription(user: UserDB, author: AuthorDB) -> bool:
        try:
            SubscriptionDB.get((SubscriptionDB.user == user) & (SubscriptionDB.author == author)).delete_instance()
            return True
        except peewee.DoesNotExist:
            return False

    @staticmethod
    def check_subscription(user: UserDB, author: AuthorDB) -> bool:
        try:
            SubscriptionDB.get((SubscriptionDB.user == user) & (SubscriptionDB.author == author))
            return True
        except peewee.DoesNotExist:
            return False

    @staticmethod
    def get_subscribers_count(author: AuthorDB) -> int:
        return int(author.subscriptions.count())
