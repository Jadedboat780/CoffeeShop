from fastapi import BackgroundTasks, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated
from annotated_types import Ge, Le

from db.database import get_async_session
from db.models import ProductOrm
from endpoints.auth import get_user_from_token
from endpoints.tasks import router


async def set_sale(percent: int, session: AsyncSession):
    query = select(ProductOrm)
    products = await session.execute(query)

    for product in products.scalars().all():
        product.price *= (percent * 0.01)

    await session.commit()


@router.post('/start_sale')
async def start_sale(
        percent: Annotated[int, Ge(5), Le(50)],
        background_tasks: BackgroundTasks,
        _authenticated=Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    '''Запуск скидок на товары'''
    background_tasks.add_task(set_sale, percent, session)
    return {'message': 'Sale start in the background'}
