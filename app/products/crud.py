from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.db.models import ProductOrm
from app.utils import Paginator
from app.products.schemas import CreateProduct, UpdateProduct, UpdateProductPartial


async def get_partial(pagination: Paginator, session: AsyncSession) -> Sequence[ProductOrm]:
    """Получение товаров"""
    query = (
        select(ProductOrm)
        .order_by(ProductOrm.id)
        .limit(pagination.limit)
        .offset(pagination.offset)
    )
    query_result = await session.execute(query)
    return query_result.scalars().all()


async def get_by_id(id: int, session: AsyncSession) -> ProductOrm | None:
    """Получение товара по id"""
    product = await session.get(ProductOrm, id)
    return product


async def get_by_category(category: str, pagination_params: Paginator, session: AsyncSession) -> Sequence[ProductOrm]:
    """Получение товаров по категории"""
    query = (
        select(ProductOrm)
        .where(category == ProductOrm.category)
        .order_by(ProductOrm.id)
        .limit(pagination_params.limit)
        .offset(pagination_params.offset)
    )
    query_result = await session.execute(query)
    return query_result.scalars().all()


async def create(new_product: CreateProduct, session: AsyncSession):
    """Создание товара"""
    insert_query = ProductOrm(**new_product.model_dump())
    session.add(insert_query)
    await session.commit()


async def update(product: ProductOrm, update_data: UpdateProduct, session: AsyncSession):
    """Полное обновление инфомации о товаре"""
    product.title = update_data.title
    product.price = update_data.price
    product.category = update_data.category
    product.description = update_data.description
    product.image_url = update_data.image_url

    await session.commit()


async def update_partial(product: ProductOrm, update_data: UpdateProductPartial, session: AsyncSession):
    """Частичное обновление инфомации о товаре"""
    if update_data.title:
        product.title = update_data.title

    if update_data.price:
        product.price = update_data.price

    if update_data.description:
        product.description = update_data.description

    if update_data.image_url:
        product.image_url = update_data.image_url

    await session.commit()


async def delete(product: ProductOrm, session: AsyncSession):
    """Удаление товара"""
    await session.delete(product)
    await session.commit()
