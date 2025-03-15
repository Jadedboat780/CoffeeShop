import uuid

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db import SessionDep, UserOrm

from .schemas import CreateUser, UpdateUserPartial
from .utils import check_password, hash_password


class UserDAO:
    """Class for accessing Users table"""

    def __init__(self, db_session: SessionDep):
        self.session = db_session

    async def get_by_id(self, *, user_id: uuid.UUID) -> UserOrm | None:
        user = await self.session.get(UserOrm, user_id)
        return user

    async def get_by_email(self, *, email: EmailStr | str, password: str) -> UserOrm | None:
        """Search user by email"""
        query = select(UserOrm).where(UserOrm.email == email)
        query_result = await self.session.execute(query)
        user = query_result.scalars().one_or_none()

        if user is None:
            return None

        if not check_password(password, user.password):
            return None

        return user

    async def create(self, *, new_user: CreateUser) -> UserOrm | None:
        """Create new user"""
        new_user.password = hash_password(new_user.password)
        user = UserOrm(**new_user.model_dump())
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            return None

    async def update_partial(self, *, user: UserOrm, update_data: UpdateUserPartial) -> UserOrm:
        """Update partial fields"""
        if update_data.new_name:
            user.name = update_data.new_name

        if update_data.new_surname:
            user.surname = update_data.new_surname

        if update_data.new_email:
            user.email = update_data.new_email

        if update_data.new_password:
            user.password = hash_password(update_data.new_password)

        if update_data.new_image_url:
            user.image_url = update_data.new_image_url

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, *, user: UserOrm) -> None:
        """Delete user"""
        await self.session.delete(user)
        await self.session.commit()
