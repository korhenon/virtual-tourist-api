from fastapi import APIRouter
from fastapi.responses import FileResponse
from data.files import FilesDataSource
from repository.files import FilesRepository

repository = FilesRepository(FilesDataSource())
router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/privacy", response_class=FileResponse)
async def get_privacy():
    return repository.get_privacy()
