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
    photo: Optional[str]
    is_subscribe: bool
    subscribers_count: int


class Route(BaseModel):
    id: int
    author: Author
    name: str
    price: int
    time: int
    description: str
    start_latitude: float
    start_longitude: float
    photo: str
    mean_mark: float


class RouteResponse(BaseModel):
    message: str
    routes: list[Route] = []
