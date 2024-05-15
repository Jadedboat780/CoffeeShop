from fastapi import APIRouter, Path, Depends, status, HTTPException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.database import get_async_session
from app.db.models import ProductOrm
from .schemas import CreateProduct, GetProduct, UpdateProduct, UpdateProductPartial

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
async def get_products(
        # limit: Annotated[int, Path(ge=0)],
        # offset: Annotated[int, Path(ge=0)],
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(ProductOrm).limit(1))
    print(result.scalars().all())
    return {"status": "success"}


@router.get("/{id}", response_model=GetProduct)
async def get_product(
        id: Annotated[int, Path(ge=1)],
        # limit: Annotated[int, Path(ge=0)],
        # offset: Annotated[int, Path(ge=0)] = 0,

        session: AsyncSession = Depends(get_async_session)
):
    result = await session.get(ProductOrm)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")
    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
        new_product: CreateProduct,
        session: AsyncSession = Depends(get_async_session)
):
    query = ProductOrm(**new_product.model_dump())
    session.add(query)
    await session.commit()
    return {"status": "success"}


@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update_product(
        id: Annotated[int, Path(ge=1)],
        update_product: UpdateProduct,
        session: AsyncSession = Depends(get_async_session)
):
    product = await session.get(ProductOrm, id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    product.title = update_product.title
    product.price = update_product.price
    product.description = update_product.description

    await session.commit()
    return {"status": "success"}


@router.patch("/{id}", status_code=status.HTTP_201_CREATED)
async def update_product_partial(
        id: Annotated[int, Path(ge=1)],
        update_product: UpdateProductPartial,
        session: AsyncSession = Depends(get_async_session)
):
    product = await session.get(ProductOrm, id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    if update_product.title:
        product.title = update_product.title

    if update_product.price:
        product.price = update_product.price

    if update_product.description:
        product.description = update_product.description

    await session.commit()
    return {"status": "success"}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        id: Annotated[int, Path(ge=1)],
        session: AsyncSession = Depends(get_async_session)
):
    product = await session.get(ProductOrm, id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    await session.delete(product)
    await session.commit()
    return {"status": "success"}
