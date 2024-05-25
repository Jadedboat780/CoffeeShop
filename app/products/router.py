from fastapi import APIRouter, Path, Depends, status, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from annotated_types import Ge, MinLen

from app.db.database import get_async_session
from app.db.models import ProductOrm
from app.auth import get_user_from_token
from app.file import is_file_exist
from .schemas import CreateProduct, GetProduct, UpdateProduct, UpdateProductPartial

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[GetProduct])
async def get_products(
        limit: Annotated[int, Ge(1)] = 100,
        offset: Annotated[int, Ge(0)] = 0,
        _authenticated = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    '''Получение всех товаров'''
    query = select(ProductOrm).order_by(ProductOrm.id).limit(limit).offset(offset)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=GetProduct)
@cache(60 * 60)
async def get_product(
        id: Annotated[int, Path(ge=1)],
        _authenticated = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    '''Получение товара'''
    result = await session.get(ProductOrm, id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")
    return result


@router.get("/category/", status_code=status.HTTP_200_OK)
# @cache(60 * 60)
async def get_products_by_category(
        category: str,
        limit: Annotated[int, Ge(1)] = 100,
        offset: Annotated[int, Ge(0)] = 0,
        _authenticated = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(ProductOrm).where(category == ProductOrm.category).order_by(ProductOrm.id).limit(limit).offset(offset)
    result = await session.execute(query)
    result = result.scalars().all()
    if len(result) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category {category} not found!")

    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
        new_product: CreateProduct,
        _authenticated = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    '''Создание товара'''
    is_exist = await is_file_exist(new_product.image_url)
    if is_exist is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You didn't add a photo")

    query = ProductOrm(**new_product.model_dump())
    session.add(query)
    await session.commit()
    return {"status": "success"}


@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update_product(
        id: Annotated[int, Path(ge=1)],
        update_product: UpdateProduct,
        _authenticated = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    '''Полное обновление информации о товаре'''
    product = await session.get(ProductOrm, id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    is_exist = await is_file_exist(update_product.image_url)
    if is_exist is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You didn't add a photo")

    product.title = update_product.title
    product.price = update_product.price
    product.category = update_product.category
    product.description = update_product.description
    product.image_url = update_product.image_url

    await session.commit()
    return {"status": "success"}


@router.patch("/{id}", status_code=status.HTTP_201_CREATED)
async def update_product_partial(
        id: Annotated[int, Path(ge=1)],
        update_product: UpdateProductPartial,
        _authenticated = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    '''Частичное обновление информации о товаре'''
    product = await session.get(ProductOrm, id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    if update_product.title:
        product.title = update_product.title

    if update_product.price:
        product.price = update_product.price

    if update_product.description:
        product.description = update_product.description

    if update_product.image_url:
        is_exist = await is_file_exist(update_product.image_url)
        if is_exist is False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You didn't add a photo")
        product.image_url = update_product.image_url

    await session.commit()
    return {"status": "success"}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        id: Annotated[int, Path(ge=1)],
        _authenticated = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    '''Удаление товара'''
    product = await session.get(ProductOrm, id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    await session.delete(product)
    await session.commit()
