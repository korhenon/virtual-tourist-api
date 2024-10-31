import datetime

from common.dto import RouteDto
from common.serializer import serialize_to_route_dto
from data.database.author import AuthorDataSource
from data.database.route import RouteDataSource
from data.database.user import UserDataSource
from data.database.work_slot import WorkSlotDataSource
from repository.auth import AuthRepository
from router.author.models import CreateChannelBody, CreateRouteBody, UpdateRouteBody, DeleteBody, \
    CreateWorkSlotBody, UpdateWorkSlotBody


class UserAlreadyHaveChannel(Exception):
    pass


class RouteDoesntExists(Exception):
    pass


class YouDontAuthorOfThisRoute(Exception):
    pass


class StartShouldBeLessThanEnd(Exception):
    pass


class SlotCanBeCreatedOnlyInFuture(Exception):
    pass


class ThisDateAlreadyBooked(Exception):
    pass


class SlotDoesntExists(Exception):
    pass


class YouDontAuthorOfThisSlot(Exception):
    pass


class AuthorRepository:
    def __init__(self, datasource: AuthorDataSource, user_datasource: UserDataSource,
                 auth_repository: AuthRepository, route_datasource: RouteDataSource, wsds: WorkSlotDataSource) -> None:
        self.ads = datasource
        self.uds = user_datasource
        self.rds = route_datasource
        self.ar = auth_repository
        self.wsds = wsds

    def create_channel(self, token: str, body: CreateChannelBody) -> None:
        user = self.uds.get_user_by_email(self.ar.authorize(token).credentials.email)
        success = self.ads.create_author(user, body.name)
        if not success:
            raise UserAlreadyHaveChannel

    def create_route(self, token: str, body: CreateRouteBody) -> None:
        author = self.ads.get_author_by_id(self.ar.authorize_author(token).id)
        self.rds.create_route(author, body.name, body.price, body.time, body.description, body.start_latitude,
                              body.start_longitude, body.photo)

    def update_route(self, token: str, body: UpdateRouteBody) -> None:
        author = self.ads.get_author_by_id(self.ar.authorize_author(token).id)
        route = self.rds.get_route_by_id(body.id)
        if route is None:
            raise RouteDoesntExists
        if route.author == author:
            self.rds.update_route(route, body.route.name, body.route.price, body.route.time,
                                  body.route.description, body.route.start_latitude,
                                  body.route.start_longitude, body.route.photo)
        else:
            raise YouDontAuthorOfThisRoute

    def delete_route(self, token: str, body: DeleteBody) -> None:
        author = self.ads.get_author_by_id(self.ar.authorize_author(token).id)
        route = self.rds.get_route_by_id(body.id)
        if route is None:
            raise RouteDoesntExists
        if route.author == author:
            self.rds.delete_route(route)
        else:
            raise YouDontAuthorOfThisRoute

    def get_routes(self, token: str) -> list[RouteDto]:
        author = self.ads.get_author_by_id(self.ar.authorize_author(token).id)
        return list(map(serialize_to_route_dto, self.rds.get_routes_by_author(author)))

    def create_slot(self, token: str, body: CreateWorkSlotBody):
        author = self.ads.get_author_by_id(self.ar.authorize_author(token).id)

        if body.start >= body.end:
            raise StartShouldBeLessThanEnd
        if body.date <= datetime.date.today():
            raise SlotCanBeCreatedOnlyInFuture
        if body.date in self.wsds.get_booked_dates(author):
            raise ThisDateAlreadyBooked
        self.wsds.create(author, body.date, body.start, body.end)

    def update_slot(self, token: str, body: UpdateWorkSlotBody):
        author = self.ads.get_author_by_id(self.ar.authorize_author(token).id)
        slot = self.wsds.get_by_id(body.id)
        if slot is None:
            raise SlotDoesntExists
        if slot.author != author:
            raise YouDontAuthorOfThisSlot
        if body.start >= body.end:
            raise StartShouldBeLessThanEnd
        self.wsds.update(slot, body.start, body.end)

    def delete_slot(self, token: str, body: DeleteBody):
        author = self.ads.get_author_by_id(self.ar.authorize_author(token).id)
        slot = self.wsds.get_by_id(body.id)
        if slot is None:
            raise SlotDoesntExists
        if slot.author != author:
            raise YouDontAuthorOfThisSlot
        self.wsds.delete(slot)
