from fastapi import APIRouter, Response

from data.database.author import AuthorDataSource
from data.database.user import UserDataSource
from repository.auth import AuthRepository, UserWithThisEmailAlreadyExist, NoUserWithThisEmail, PasswordIsNotCorrect
from router.auth.models import RegistrationBody, TokenResponse, LoginBody

repository = AuthRepository(UserDataSource(), AuthorDataSource())
router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post("/registration", status_code=201)
async def register_user(body: RegistrationBody, response: Response) -> TokenResponse:
    try:
        token = repository.create_user(body)
        return TokenResponse(message="Успех!", token=token)
    except UserWithThisEmailAlreadyExist:
        response.status_code = 400
        return TokenResponse(message="Пользователь с такой почтой уже зарегестрирован!")


@router.post("/login", status_code=200)
async def login(body: LoginBody, response: Response):
    try:
        token = repository.login(body)
        return TokenResponse(message="Успех!", token=token)
    except NoUserWithThisEmail:
        response.status_code = 400
        return TokenResponse(message="Пользователя с такой почтой не существует!")
    except PasswordIsNotCorrect:
        response.status_code = 400
        return TokenResponse(message="Неверный пароль!")
