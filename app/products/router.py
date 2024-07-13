from fastapi import APIRouter, Path, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.products.schemas import GetProduct, CreateProduct, UpdateProduct, UpdateProductPartial
import app.products.crud as product_crud
from app.db.database import get_async_session
from app.utils import Paginator
from app.auth import get_user_from_token

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/{id}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_user_from_token)], response_model=GetProduct, summary='Получить продукт')
async def get_product(
        id: Annotated[int, Path(ge=1)],
        session: AsyncSession = Depends(get_async_session)
):
    result = await product_crud.get_by_id(id, session)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    return result


@router.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(get_user_from_token)], response_model=list[GetProduct], summary='Получить продукты')
async def get_products(
        pagination: Paginator = Depends(),
        session: AsyncSession = Depends(get_async_session)
):
    data = await product_crud.get_partial(pagination, session)
    return data


@router.get("/category/", status_code=status.HTTP_200_OK, dependencies=[Depends(get_user_from_token)], response_model=list[GetProduct],
            summary='Получить продукты по категории')
async def get_products_by_category(
        category: str,
        pagination: Paginator = Depends(),
        session: AsyncSession = Depends(get_async_session)
):
    data = await product_crud.get_by_category(category, pagination, session)
    if len(data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category {category} not found!")

    return data


@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_user_from_token)], summary='Создать продукт')
async def create_product(
        new_product: CreateProduct,
        session: AsyncSession = Depends(get_async_session)
):
    await product_crud.create(new_product, session)
    return {"status": "success"}


@router.put("/{id}", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_user_from_token)], summary='Обновить информацию о продукте')
async def update_product(
        id: Annotated[int, Path(ge=1)],
        update_data: UpdateProduct,
        session: AsyncSession = Depends(get_async_session)
):
    product = await product_crud.get_by_id(id, session)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    await product_crud.update(product, update_data, session)
    return {"status": "success"}


@router.patch("/{id}", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_user_from_token)], summary='Обновить часть информации о продукте')
async def update_product_partial(
        id: Annotated[int, Path(ge=1)],
        update_data: UpdateProductPartial,
        session: AsyncSession = Depends(get_async_session)
):
    product = await product_crud.get_by_id(id, session)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    await product_crud.update_partial(product, update_data, session)
    return {"status": "success"}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_user_from_token)], summary='Удалить продукт')
async def delete_product(
        id: Annotated[int, Path(ge=1)],
        session: AsyncSession = Depends(get_async_session)
):
    product = await product_crud.get_by_id(id, session)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    await product_crud.delete(product, session)
