# from fastapi import APIRouter, File, UploadFile
#
# router = APIRouter(prefix="/files", tags=["Files"])
#
# @router.post("/")
# async def create_file(file: bytes = File()):
#     return {"file_size": len(file)}
#
#
# @router.post("/upload")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}