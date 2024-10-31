import datetime

from pydantic import BaseModel


class CreateChannelBody(BaseModel):
    name: str


class CreateRouteBody(BaseModel):
    name: str
    price: int
    time: int
    description: str
    start_latitude: float
    start_longitude: float
    photo: str


class UpdateRouteBody(BaseModel):
    id: int
    route: CreateRouteBody


class DeleteBody(BaseModel):
    id: int


class Route(BaseModel):
    id: int
    name: str
    price: int
    time: int
    description: str
    start_latitude: float
    start_longitude: float
    photo: str


class RoutesResponse(BaseModel):
    message: str
    routes: list[Route]


class CreateWorkSlotBody(BaseModel):
    date: datetime.date
    start: datetime.time
    end: datetime.time


class UpdateWorkSlotBody(BaseModel):
    id: int
    start: datetime.time
    end: datetime.time



