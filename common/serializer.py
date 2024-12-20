import datetime
from typing import Any, Optional

from common.dto import UserDto, CredentialsDto, AuthorDto, RouteDto, CommentDto
from data.database import AuthorDB, RouteDB, CommentDB
from data.database.user import UserDB
from router.auth.models import RegistrationBody, LoginBody


def serialize_to_user_dto(obj: Any) -> Optional[UserDto]:
    t = type(obj)
    if t is UserDB:
        return UserDto(name=obj.name,
                       credentials=CredentialsDto(email=obj.email, password=obj.password),
                       photo=None if obj.photo is None else obj.photo.id)
    elif t is RegistrationBody:
        return UserDto(name=obj.name,
                       credentials=CredentialsDto(email=obj.email, password=obj.password),
                       photo=None)
    return None


def serialize_to_credentials_dto(obj: Any) -> Optional[CredentialsDto]:
    t = type(obj)
    if t is LoginBody:
        return CredentialsDto(email=obj.email, password=obj.password)
    return None


def serialize_to_author_dto(obj: Any) -> Optional[AuthorDto]:
    t = type(obj)
    if t is AuthorDB:
        return AuthorDto(obj.id, serialize_to_user_dto(obj.user), obj.name, obj.description)
    return None


def serialize_to_route_dto(obj: Any) -> Optional[RouteDto]:
    t = type(obj)
    if t is RouteDB:
        return RouteDto(obj.id, obj.name, obj.price, obj.time, obj.description, obj.start_latitude,
                        obj.start_longitude, None if obj.photo is None else obj.photo.id)
    return None


def serialize_to_comment_dto(obj: Any) -> Optional[CommentDto]:
    t = type(obj)
    if t is CommentDB:
        return CommentDto(obj.id, serialize_to_route_dto(obj.route), serialize_to_user_dto(obj.user),
                          obj.created_at.date(), obj.mark, obj.text)
    return None
