import datetime
from typing import Optional

from pydantic import BaseModel


class SubscriptionBody(BaseModel):
    author_id: int


class TimeForReservation(BaseModel):
    start: datetime.time
    presentation: str


class SlotWithTimesForReservation(BaseModel):
    id: int
    date: datetime.date
    times: list[TimeForReservation]


class ReservationBody(BaseModel):
    route_id: int
    slot_id: int
    start: datetime.time


class Author(BaseModel):
    id: int
    name: str
    photo: Optional[int]
    is_subscribe: bool
    subscribers_count: int


class Route(BaseModel):
    id: int
    author: Author
    name: str
    price: int
    time: int
    description: str
    photo: int
    mean_mark: float


class CommentUser(BaseModel):
    name: str
    photo: Optional[int]


class Comment(BaseModel):
    user: CommentUser
    date: datetime.date
    mark: int
    text: str


class FullRoute(BaseModel):
    id: int
    author: Author
    name: str
    price: int
    time: int
    description: str
    photo: int
    mean_mark: float
    comments_count: int
    comments: list[Comment]


class FullRouteResponse(BaseModel):
    message: str
    route: Optional[FullRoute] = None


class RouteResponse(BaseModel):
    message: str
    routes: list[Route] = []
