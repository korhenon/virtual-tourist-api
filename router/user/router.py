from fastapi import APIRouter, Response

from common.dto import RouteForUser
from data.database.author import AuthorDataSource
from data.database.reservations import ReservationsDataSource
from data.database.route import RouteDataSource
from data.database.subscription import SubscriptionDataSource
from data.database.user import UserDataSource
from data.database.work_slot import WorkSlotDataSource
from repository.auth import AuthRepository, NotAuthorized
from repository.user import UserRepository, UserAlreadyHaveSubscribedToAuthor, UserDidntSubscribedToAuthor, \
    ThisTimeAlreadyReserved, RouteAndSlotAuthorsDontEqual, RouteDoesntExists, SlotDoesntExists, ThisTimeNotInSlotBorders
from router.models import TokenHeader, MessageResponse
from router.user.models import SubscriptionBody, TimeForReservation, SlotWithTimesForReservation, ReservationBody, \
    RouteResponse, Route, Author

repository = UserRepository(UserDataSource(), AuthorDataSource(), SubscriptionDataSource(),
                            AuthRepository(UserDataSource(), AuthorDataSource()), RouteDataSource(),
                            WorkSlotDataSource(), ReservationsDataSource())
router = APIRouter(prefix="/user", tags=["User"])


@router.post("/subscribe")
async def subscribe_to_author(body: SubscriptionBody, response: Response, token: TokenHeader = None) -> MessageResponse:
    try:
        repository.subscribe(token, body)
        return MessageResponse(message="Успех!")
    except UserAlreadyHaveSubscribedToAuthor:
        response.status_code = 400
        return MessageResponse(message="Пользователь уже подписан на этого автора!")
    except NotAuthorized:
        response.status_code = 401
        return MessageResponse(message="Не авторизованный запрос!")


@router.post("/unsubscribe")
async def unsubscribe_to_author(body: SubscriptionBody, response: Response,
                                token: TokenHeader = None) -> MessageResponse:
    try:
        repository.unsubscribe(token, body)
        return MessageResponse(message="Успех!")
    except UserDidntSubscribedToAuthor:
        response.status_code = 400
        return MessageResponse(message="Пользователь не подписан на этого автора!")
    except NotAuthorized:
        response.status_code = 401
        return MessageResponse(message="Не авторизованный запрос!")


@router.get("/times_for_reservation/{route_id}")
async def get_times_for_reservation(route_id: int) -> list[SlotWithTimesForReservation]:
    return list(map(lambda x: SlotWithTimesForReservation(id=x.slot_id, date=x.date, times=map(
        lambda y: TimeForReservation(start=y.start, presentation=y.string), x.times)),
                    repository.get_times_for_order(route_id)))


@router.post("/reservation")
async def create_reservation(body: ReservationBody, response: Response, token: TokenHeader = None) -> MessageResponse:
    try:
        repository.create_reservation(token, body)
        return MessageResponse(message="Успех!")
    except RouteDoesntExists:
        response.status_code = 400
        return MessageResponse(message="Маршрут не существует!")
    except SlotDoesntExists:
        response.status_code = 400
        return MessageResponse(message="Слот не существует!")
    except ThisTimeAlreadyReserved:
        response.status_code = 400
        return MessageResponse(message="Это время уже зарезервировано выберите другое!")
    except RouteAndSlotAuthorsDontEqual:
        response.status_code = 400
        return MessageResponse(message="У пользователя и слота не совпадают авторы!")
    except ThisTimeNotInSlotBorders:
        response.status_code = 400
        return MessageResponse(message="Выбранное время не входит в слот!")
    except NotAuthorized:
        response.status_code = 401
        return MessageResponse(message="Не авторизованный запрос!")


@router.get("/recommendations")
async def get_recommendations(response: Response, token: TokenHeader = None) -> RouteResponse:
    try:
        routes = repository.get_routes(token)
        return RouteResponse(message="Успех!", routes=list(
            map(lambda x:
                Route(
                    id=x.route.id,
                    author=Author(
                        id=x.author.id,
                        name=x.author.name,
                        photo=x.author.user.photo,
                        is_subscribe=x.is_user_subscribed,
                        subscribers_count=x.author_subscribers,
                    ),
                    name=x.route.name,
                    price=x.route.price,
                    time=x.route.time,
                    description=x.route.description,
                    start_latitude=x.route.start_latitude,
                    start_longitude=x.route.start_longitude,
                    photo=x.route.photo,
                    mean_mark=x.mean_mark), routes)))
    except NotAuthorized:
        response.status_code = 401
        return RouteResponse(message="Не авторизованный запрос!")
