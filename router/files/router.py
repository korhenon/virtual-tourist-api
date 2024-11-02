from typing import Optional

from fastapi import APIRouter, UploadFile, Response
from fastapi.responses import FileResponse

from data.database.author import AuthorDataSource
from data.database.user import UserDataSource
from data.files import FilesDataSource
from repository.auth import AuthRepository, NotAuthorized
from repository.files import FilesRepository, FileNotFound
from router.models import TokenHeader, MessageResponse

repository = FilesRepository(FilesDataSource(), AuthRepository(UserDataSource(), AuthorDataSource()))
router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/privacy", response_class=FileResponse)
async def get_privacy():
    return repository.get_privacy()


@router.post("/photos")
async def upload_photo(file: UploadFile, response: Response, token: TokenHeader = None) -> MessageResponse:
    try:
        return MessageResponse(message=repository.upload_photo(token, await file.read()))
    except NotAuthorized:
        response.status_code = 401
        return MessageResponse(message="Не авторизированный запрос!")


@router.get("/photos/{filename}", response_model=None)
async def get_photo(filename: str) -> Optional[FileResponse]:
    try:
        return FileResponse(repository.get_file(filename))
    except FileNotFound:
        return None
