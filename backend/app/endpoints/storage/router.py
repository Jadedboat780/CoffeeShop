from fastapi import APIRouter, UploadFile, Response, Depends

from endpoints.storage.storage import storage
from endpoints.auth import get_user_from_token

router = APIRouter(prefix="/storage", tags=["Storage"], dependencies=[Depends(get_user_from_token)])


@router.post("/upload", summary='Загрузка файла в хранилище')
async def upload_file(file: UploadFile):
    await storage.upload_file(file)
    return {'file': file.filename}


@router.get("/", summary='Получение файла из хранилища')
async def get_file(file_name: str):
    file = await storage.get_file(file_name)
    return Response(content=file, media_type="image/png")
