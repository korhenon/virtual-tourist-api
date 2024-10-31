import datetime

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
