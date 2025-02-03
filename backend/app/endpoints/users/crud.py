from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from endpoints.users.schemas import GetUser, CreateUser, UpdateUserPartial
from db.models import UserOrm
from utils import hash_password, check_password


async def get(entered_user: GetUser, session: AsyncSession) -> UserOrm | None:
    """Поиск юзера"""
    query = select(UserOrm).where(entered_user.email == UserOrm.email)
    query_result = await session.execute(query)
    data = query_result.scalars().one_or_none()
    if data is None:
        return None

    if not check_password(entered_user.password, data.password):
        return None

    return data


async def create(new_user: CreateUser, session: AsyncSession) -> bool:
    """Создание нового юзера"""
    new_user.password = hash_password(new_user.password)
    query = UserOrm(**new_user.model_dump())
    try:
        session.add(query)
        await session.commit()
        return True
    except IntegrityError:
        return False


async def update_partial(user: UserOrm, update_data: UpdateUserPartial, session: AsyncSession) -> None:
    """Обновление данных о юзере"""
    if update_data.name:
        user.name = update_data.name

    if update_data.surname:
        user.surname = update_data.surname

    if update_data.email:
        user.email = update_data.email

    if update_data.password:
        user.password = hash_password(update_data.password)

    if update_data.image_url:
        user.image_url = update_data.image_url

    await session.commit()


async def delete(user: UserOrm, session: AsyncSession) -> None:
    """Удаление юзера"""
    await session.delete(user)
    await session.commit()
