from aiobotocore.session import get_session, AioSession, AioBaseClient
from fastapi import UploadFile, HTTPException, status

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.config import settings


class Storage:
    __slots__ = ('config', 'bucket_name', 'session')

    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name: str = bucket_name
        self.session: AioSession = get_session()

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[AioBaseClient, None]:
        """Получение сессии"""
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def get_files_list(self) -> list[str]:
        """Получение списка всех файлов в хранилище"""
        async with self.get_client() as client:
            paginator = client.get_paginator('list_objects')
            async for result in paginator.paginate(Bucket=self.bucket_name, Prefix=''):
                return [key['Key'] for key in result.get('Contents')]

    async def get_file(self, file_name: str) -> bytes:
        """Получение файла из хранилища"""
        async with self.get_client() as client:
            try:
                response = await client.get_object(Bucket=self.bucket_name, Key=file_name)
                data: bytes = await response["Body"].read()
                return data
            except:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found')

    async def upload_file(self, file: UploadFile):
        """Загрузка файла в хранилище"""
        async with self.get_client() as client:
            await client.put_object(Bucket=self.bucket_name, Key=file.filename, Body=await file.read())

    async def delete_file(self, file_name: str):
        """Удаление файла из хранилища"""
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=file_name)

    def __repr__(self):
        return f'Storage "{self.bucket_name}"'


storage = Storage(access_key=settings.S3_ACCESS_KEY,
                  secret_key=settings.S3_SECRET_KEY,
                  endpoint_url=settings.S3_ENDPOINT_URL,
                  bucket_name=settings.S3_BUCKET_NAME)
