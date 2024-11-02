from typing import Optional

import peewee

from data.database import AuthorDB, RouteDB


class RouteDataSource:
    @staticmethod
    def get_routes_by_author(author: AuthorDB) -> list[RouteDB]:
        return list(author.routes)

    @staticmethod
    def get_routes() -> list[RouteDB]:
        return list(RouteDB.select())

    @staticmethod
    def get_route_by_id(_id: int) -> Optional[RouteDB]:
        try:
            return RouteDB.get(RouteDB.id == _id)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def create_route(author: AuthorDB, name: str, price: int, time: int, description: str,
                     start_latitude: float, start_longitude: float, photo: str) -> None:
        RouteDB(author=author, name=name, price=price, time=time, description=description,
                start_latitude=start_latitude, start_longitude=start_longitude, photo=photo).save()

    @staticmethod
    def update_route(route: RouteDB, name: str, price: int, time: int, description: str,
                     start_latitude: float, start_longitude: float, photo: str) -> bool:
        try:
            route.name = name
            route.price = price
            route.time = time
            route.description = description
            route.start_latitude = start_latitude
            route.start_longitude = start_longitude
            route.photo = photo
            route.save()
            return True
        except peewee.DoesNotExist:
            return False

    @staticmethod
    def delete_route(route: RouteDB) -> bool:
        try:
            route.delete_instance()
            return True
        except peewee.DoesNotExist:
            return False
