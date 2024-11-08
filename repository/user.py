import datetime
import math

from common.dto import TimeForReservationDto, SlotWithReservationsDto, RouteForUser, RouteFull
from common.serializer import serialize_to_route_dto, serialize_to_author_dto, serialize_to_comment_dto
from data.database import CommentDB
from data.database.author import AuthorDataSource
from data.database.comment import CommentDataSource
from data.database.reservations import ReservationsDataSource
from data.database.route import RouteDataSource
from data.database.subscription import SubscriptionDataSource
from data.database.user import UserDataSource
from data.database.work_slot import WorkSlotDataSource
from repository.auth import AuthRepository
from repository.author import RouteDoesntExists, SlotDoesntExists
from router.user.models import SubscriptionBody, ReservationBody


class UserAlreadyHaveSubscribedToAuthor(Exception):
    pass


class UserDidntSubscribedToAuthor(Exception):
    pass


class RouteAndSlotAuthorsDontEqual(Exception):
    pass


class ThisTimeAlreadyReserved(Exception):
    pass


class ThisTimeNotInSlotBorders(Exception):
    pass


class UserRepository:
    def __init__(self, uds: UserDataSource, ads: AuthorDataSource, sds: SubscriptionDataSource,
                 ar: AuthRepository, rds: RouteDataSource, wsds: WorkSlotDataSource,
                 reds: ReservationsDataSource, cds: CommentDataSource) -> None:
        self.uds = uds
        self.ads = ads
        self.sds = sds
        self.rds = rds
        self.wsds = wsds
        self.reds = reds
        self.ar = ar
        self.cds = cds

    def subscribe(self, token: str, body: SubscriptionBody) -> None:
        user = self.uds.get_user_by_email(self.ar.authorize(token).credentials.email)
        author = self.ads.get_author_by_id(body.author_id)

        success = self.sds.create_subscription(user, author)

        if not success:
            raise UserAlreadyHaveSubscribedToAuthor

    def unsubscribe(self, token: str, body: SubscriptionBody) -> None:
        user = self.uds.get_user_by_email(self.ar.authorize(token).credentials.email)
        author = self.ads.get_author_by_id(body.author_id)

        success = self.sds.delete_subscription(user, author)

        if not success:
            raise UserDidntSubscribedToAuthor

    @staticmethod
    def get_minutes_from_time(t: datetime.time) -> int:
        return t.hour * 60 + t.minute

    @staticmethod
    def get_time_from_minutes(m: int) -> datetime.time:
        return datetime.time(m // 60, m % 60)

    @staticmethod
    def get_times_for_gap(start: int, end: int, duration: int) -> list[TimeForReservationDto]:
        times = []
        for i in range(math.floor((end - start) / duration)):
            _start = UserRepository.get_time_from_minutes(start + i * duration)
            _end = UserRepository.get_time_from_minutes(start + (i + 1) * duration)
            _start_minutes = _start.minute if _start.minute >= 10 else f"0{_start.minute}"
            _end_minutes = _end.minute if _end.minute >= 10 else f"0{_end.minute}"
            times.append(TimeForReservationDto(_start, f"{_start.hour}:{_start_minutes}—{_end.hour}:{_end_minutes}"))
        return times

    def get_times_for_order(self, route_id: int) -> list[SlotWithReservationsDto]:
        route = self.rds.get_route_by_id(route_id)
        if route is None:
            raise RouteDoesntExists
        slots = self.wsds.get_upcoming(route.author)
        slots_with_reservation_times = []
        for slot in slots:
            times = []
            reservations = self.reds.get_by_slot(slot)
            last_end = self.get_minutes_from_time(slot.start)
            for reservation in reservations:
                print(self.get_minutes_from_time(reservation.start))
                times += self.get_times_for_gap(last_end, self.get_minutes_from_time(reservation.start), route.time)
                last_end = self.get_minutes_from_time(reservation.start) + reservation.route.time
            times += self.get_times_for_gap(last_end, self.get_minutes_from_time(slot.end), route.time)
            if len(times) > 0:
                slots_with_reservation_times.append(SlotWithReservationsDto(slot.id, slot.date, times))
        return slots_with_reservation_times

    def create_reservation(self, token: str, body: ReservationBody):
        user = self.uds.get_user_by_email(self.ar.authorize(token).credentials.email)
        route = self.rds.get_route_by_id(body.route_id)
        slot = self.wsds.get_by_id(body.slot_id)
        if route is None:
            raise RouteDoesntExists
        if slot is None:
            raise SlotDoesntExists
        if route.author != slot.author:
            raise RouteAndSlotAuthorsDontEqual
        new_reservation_start = self.get_minutes_from_time(body.start)
        new_reservation_end = new_reservation_start + route.time
        if not ((self.get_minutes_from_time(slot.start) <= new_reservation_start) and
                (new_reservation_end <= self.get_minutes_from_time(slot.end))):
            raise ThisTimeNotInSlotBorders
        for reservation in slot.reservations:
            reservation_start = self.get_minutes_from_time(reservation.start)
            reservation_end = reservation_start + reservation.route.time
            if reservation_start > new_reservation_start:
                if new_reservation_end > reservation_start:
                    raise ThisTimeAlreadyReserved
            elif reservation_start < new_reservation_start:
                if reservation_end > new_reservation_start:
                    raise ThisTimeAlreadyReserved
            else:
                raise ThisTimeAlreadyReserved
        self.reds.create(user, route, body.start, slot)

    def get_routes(self, token: str) -> list[RouteForUser]:
        user = self.uds.get_user_by_email(self.ar.authorize(token).credentials.email)
        routes = list(map(lambda x: RouteForUser(
            serialize_to_route_dto(x),
            serialize_to_author_dto(x.author),
            self.sds.get_subscribers_count(x.author),
            self.sds.check_subscription(user, x.author),
            self.cds.get_mean_mark(x)
        ), self.rds.get_routes()))
        return routes

    def get_full_route_info(self, token: str, route_id: int) -> RouteFull:
        user = self.uds.get_user_by_email(self.ar.authorize(token).credentials.email)
        route = self.rds.get_route_by_id(route_id)
        if route is None:
            raise RouteDoesntExists
        comments = self.cds.get_comments(route)
        return RouteFull(
            serialize_to_route_dto(route),
            serialize_to_author_dto(route.author),
            self.sds.get_subscribers_count(route.author),
            self.sds.check_subscription(user, route.author),
            self.cds.get_mean_mark(route),
            len(comments),
            list(map(serialize_to_comment_dto, comments))
        )
