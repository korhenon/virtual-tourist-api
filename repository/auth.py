from common.dto import UserDto, AuthorDto
from common.serializer import serialize_to_user_dto, serialize_to_credentials_dto, serialize_to_author_dto
from data.database.author import AuthorDataSource
from data.database.user import UserDataSource
from data.jwt import JWTDataSource
from router.auth.models import RegistrationBody, LoginBody


class UserWithThisEmailAlreadyExist(Exception):
    pass


class PasswordIsNotCorrect(Exception):
    pass


class NoUserWithThisEmail(Exception):
    pass


class NotAuthorized(Exception):
    pass


class UserDoesntHaveChannel(Exception):
    pass


class AuthRepository:
    def __init__(self, datasource: UserDataSource, author_datasource: AuthorDataSource) -> None:
        self.ds = datasource
        self.ads = author_datasource

    def create_user(self, body: RegistrationBody) -> str:
        new_user = serialize_to_user_dto(body)
        success = self.ds.create_user(new_user.name, new_user.credentials.email, new_user.credentials.password)
        if success:
            return JWTDataSource.encode(new_user.credentials.email)
        else:
            raise UserWithThisEmailAlreadyExist()

    def login(self, body: LoginBody):
        credentials = serialize_to_credentials_dto(body)
        user = serialize_to_user_dto(self.ds.get_user_by_email(credentials.email))
        if user is not None:
            if user.credentials.password == credentials.password:
                return JWTDataSource.encode(user.credentials.email)
            raise PasswordIsNotCorrect
        raise NoUserWithThisEmail

    def authorize(self, token: str) -> UserDto:
        user = serialize_to_user_dto(self.ds.get_user_by_email(JWTDataSource.decode(token)))
        if user is not None:
            return user
        raise NotAuthorized

    def authorize_author(self, token: str) -> AuthorDto:
        user = self.ds.get_user_by_email(self.authorize(token).credentials.email)
        author = serialize_to_author_dto(self.ads.get_author_by_user(user))
        if author is not None:
            return author
        raise UserDoesntHaveChannel
