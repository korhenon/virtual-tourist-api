from typing import Optional

from fastapi import APIRouter, UploadFile, Response
from fastapi.responses import FileResponse

from data.database.author import AuthorDataSource
from data.database.file import FileDataSource
from data.database.user import UserDataSource
from repository.auth import AuthRepository, NotAuthorized
from repository.files import FilesRepository, FileNotFound
from router.models import TokenHeader, MessageResponse

repository = FilesRepository(FileDataSource(), AuthRepository(UserDataSource(), AuthorDataSource()))
router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/privacy", response_class=FileResponse)
async def get_privacy():
    return "privacy.pdf"


@router.post("/photos")
async def upload_photo(file: UploadFile, response: Response, token: TokenHeader = None) -> MessageResponse:
    try:
        return MessageResponse(message=str(repository.upload_photo(token, await file.read())))
    except NotAuthorized:
        response.status_code = 401
        return MessageResponse(message="Не авторизированный запрос!")


@router.get("/photos/{file_id}", response_model=None)
async def get_photo(file_id: int) -> Optional[Response]:
    try:
        return Response(content=repository.get_file(file_id), media_type="image/png")
    except FileNotFound:
        return None
