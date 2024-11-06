from fastapi import APIRouter, Response

from data.database.author import AuthorDataSource
from data.database.file import FileDataSource
from data.database.route import RouteDataSource
from data.database.user import UserDataSource
from data.database.work_slot import WorkSlotDataSource
from repository.auth import AuthRepository, NotAuthorized, UserDoesntHaveChannel
from repository.author import AuthorRepository, UserAlreadyHaveChannel, YouDontAuthorOfThisRoute, RouteDoesntExists, \
    ThisDateAlreadyBooked, SlotCanBeCreatedOnlyInFuture, StartShouldBeLessThanEnd, SlotDoesntExists, \
    YouDontAuthorOfThisSlot
from repository.files import FileNotFound
from router.author.models import CreateChannelBody, CreateRouteBody, UpdateRouteBody, DeleteBody, RoutesResponse, \
    Route, CreateWorkSlotBody, UpdateWorkSlotBody
from router.models import TokenHeader, MessageResponse

repository = AuthorRepository(AuthorDataSource(), UserDataSource(),
                              AuthRepository(UserDataSource(), AuthorDataSource()), RouteDataSource(),
                              WorkSlotDataSource(), FileDataSource())
router = APIRouter(prefix="/author", tags=["Author"])


@router.post("/create_channel", status_code=201)
async def create_channel(body: CreateChannelBody, response: Response, token: TokenHeader = None) -> MessageResponse:
    try:
        repository.create_channel(token, body)
        return MessageResponse(message="Успех!")
    except UserAlreadyHaveChannel:
        response.status_code = 400
        return MessageResponse(message="Этот пользователь уже имеет канал!")
    except NotAuthorized:
        response.status_code = 401
        return MessageResponse(message="Не авторизованный запрос!")


@router.get("/routes")
async def get_routes(response: Response, token: TokenHeader = None) -> RoutesResponse:
    try:
        routes = list(map(lambda x: Route(
            id=x.id,
            name=x.name,
            price=x.price,
            time=x.time,
            description=x.description,
            start_latitude=x.start_latitude,
            start_longitude=x.start_longitude,
            photo=x.photo
        ), repository.get_routes(token)))
        return RoutesResponse(message="Успех!", routes=routes)
    except UserDoesntHaveChannel:
        response.status_code = 400
        return RoutesResponse(message="Пользователь не имеет канала!")
    except NotAuthorized:
        response.status_code = 401
        return RoutesResponse(message="Не авторизованный запрос!")


@router.post("/route", status_code=201)
async def create_route(body: CreateRouteBody, response: Response, token: TokenHeader = None) -> MessageResponse:
    try:
        repository.create_route(token, body)
        return MessageResponse(message="Успех!")
    except NotAuthorized:
        response.status_code = 401
        return MessageResponse(message="Не авторизованный запрос!")
    except UserDoesntHaveChannel:
        response.status_code = 400
        return MessageResponse(message="Пользователь не имеет канала!")
    except FileNotFound:
        response.status_code = 400
        return MessageResponse(message="Файл фотографии не найден!")


@router.put("/route")
async def update_route(body: UpdateRouteBody, response: Response, token: TokenHeader = None) -> MessageResponse:
    try:
        repository.update_route(token, body)
        return MessageResponse(message="Успех!")
    except YouDontAuthorOfThisRoute:
        response.status_code = 400
        return MessageResponse(message="Вы не автор этого маршрута!")
    except RouteDoesntExists:
        response.status_code = 400
        return MessageResponse(message="Маршрут не существует!")
    except NotAuthorized:
        response.status_code = 401
        return MessageResponse(message="Не авторизованный запрос!")
    except UserDoesntHaveChannel:
        response.status_code = 400
        return MessageResponse(message="Пользователь не имеет канала!")
    except FileNotFound:
        response.status_code = 400
        return MessageResponse(message="Файл фотографии не найден!")


@router.delete("/route")
async def delete_route(body: DeleteBody, response: Response, token: TokenHeader = None) -> MessageResponse:
    try:
        repository.delete_route(token, body)
        return MessageResponse(message="Успех!")
    except YouDontAuthorOfThisRoute:
        response.status_code = 400
        return MessageResponse(message="Вы не автор этого маршрута!")
    except RouteDoesntExists:
        response.status_code = 400
        return MessageResponse(message="Маршрут не существует!")
    except NotAuthorized:
        response.status_code = 401
        return MessageResponse(message="Не авторизованный запрос!")
    except UserDoesntHaveChannel:
        response.status_code = 400
        return MessageResponse(message="Пользователь не имеет канала!")


@router.post("/slot", status_code=201)
async def create_slot(body: CreateWorkSlotBody, response: Response, token: TokenHeader = None) -> MessageResponse:
    try:
        repository.create_slot(token, body)
        return MessageResponse(message="Успех!")
    except ThisDateAlreadyBooked:
        response.status_code = 400
        return MessageResponse(message="Данная дата уже забронирована!")
    except StartShouldBeLessThanEnd:
        response.status_code = 400
        return MessageResponse(message="Время старта должно быть меньше времени окончания!")
    except SlotCanBeCreatedOnlyInFuture:
        response.status_code = 400
        return MessageResponse(message="Слот может быть создан только в будущем!")
    except NotAuthorized:
        response.status_code = 401
        return MessageResponse(message="Не авторизованный запрос!")
    except UserDoesntHaveChannel:
        response.status_code = 400
        return MessageResponse(message="Пользователь не имеет канала!")


@router.put("/slot")
async def update_slot(body: UpdateWorkSlotBody, response: Response, token: TokenHeader = None) -> MessageResponse:
    try:
        repository.update_slot(token, body)
        return MessageResponse(message="Успех!")
    except StartShouldBeLessThanEnd:
        response.status_code = 400
        return MessageResponse(message="Время старта должно быть меньше времени окончания!")
    except YouDontAuthorOfThisSlot:
        response.status_code = 400
        return MessageResponse(message="Вы не являетесь автором данного слота!")
    except SlotDoesntExists:
        response.status_code = 400
        return MessageResponse(message="Слот не существует!")
    except NotAuthorized:
        response.status_code = 401
        return MessageResponse(message="Не авторизованный запрос!")
    except UserDoesntHaveChannel:
        response.status_code = 400
        return MessageResponse(message="Пользователь не имеет канала!")


@router.delete("/slot")
async def delete_slot(body: DeleteBody, response: Response, token: TokenHeader = None) -> MessageResponse:
    try:
        repository.delete_slot(token, body)
        return MessageResponse(message="Успех!")
    except YouDontAuthorOfThisSlot:
        response.status_code = 400
        return MessageResponse(message="Вы не являетесь автором данного слота!")
    except SlotDoesntExists:
        response.status_code = 400
        return MessageResponse(message="Слот не существует!")
    except NotAuthorized:
        response.status_code = 401
        return MessageResponse(message="Не авторизованный запрос!")
    except UserDoesntHaveChannel:
        response.status_code = 400
        return MessageResponse(message="Пользователь не имеет канала!")
