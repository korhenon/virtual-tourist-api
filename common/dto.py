import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class CredentialsDto:
    email: str
    password: str


@dataclass
class UserDto:
    name: str
    credentials: CredentialsDto
    photo: Optional[str]


@dataclass
class AuthorDto:
    id: int
    user: UserDto
    name: str
    description: str


@dataclass
class RouteDto:
    id: int
    name: str
    price: int
    time: int
    description: str
    start_latitude: float
    start_longitude: float
    photo: int


@dataclass
class TimeForReservationDto:
    start: datetime.time
    string: str


@dataclass
class SlotWithReservationsDto:
    slot_id: int
    date: datetime.date
    times: list[TimeForReservationDto]


@dataclass
class CommentDto:
    id: int
    route: RouteDto
    user: UserDto
    date: datetime.date
    mark: int
    text: str


@dataclass
class RouteForUser:
    route: RouteDto
    author: AuthorDto
    author_subscribers: int
    is_user_subscribed: bool
    mean_mark: float


@dataclass
class RouteFull:
    route: RouteDto
    author: AuthorDto
    author_subscribers: int
    is_user_subscribed: bool
    mean_mark: float
    comments_count: int
    comments: list[CommentDto]
