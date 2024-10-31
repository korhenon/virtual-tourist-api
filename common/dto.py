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
    photo: str


@dataclass
class TimeForReservationDto:
    start: datetime.time
    string: str


@dataclass
class SlotWithReservationsDto:
    slot_id: int
    date: datetime.date
    times: list[TimeForReservationDto]
