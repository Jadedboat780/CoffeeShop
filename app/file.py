from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
import aiofiles
import aiofiles.os as aos

router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/")
async def get_file(file_name: str):
    '''Получение необходимого файла по названию'''
    try:
        return FileResponse(f'files/{file_name}')
    except FileNotFoundError:
        return {'error': 'File not found'}


@router.post("/")
async def create_file(file: UploadFile):
    '''Сохранение файла'''
    async with aiofiles.open(f'files/{file.filename}', "wb") as new_file:
        content = await file.read()
        await new_file.write(content)
    return file.filename

async def is_file_exist(file_name: str) -> bool:
    '''Проверка существования файла'''
    content = await aos.listdir('files')
    return file_name in content