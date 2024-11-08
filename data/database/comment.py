from peewee import fn

from data.database import RouteDB, CommentDB


class CommentDataSource:
    @staticmethod
    def get_mean_mark(route: RouteDB) -> float:
        result = CommentDB.select(fn.AVG(CommentDB.mark)).where(CommentDB.route == route).scalar()
        if result is None:
            return 0
        else:
            return round(result, 1)

    @staticmethod
    def get_comments(route: RouteDB) -> list[CommentDB]:
        return list(route.comments)
