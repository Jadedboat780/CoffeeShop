from sqlalchemy import select

from app.db import CoffeeOrm, SessionDep
from app.db.models import CoffeeCategory
from app.endpoints.pagination import Paginator
from .schemas import CreateCoffee, UpdateCoffee, UpdateCoffeePartial


class CoffeeDAO:
    """Class for accessing Coffees table"""

    def __init__(self, db_session: SessionDep):
        self.session = db_session

    async def get_partial(self, *, pagination: Paginator) -> list[CoffeeOrm]:
        """Get coffees"""
        query = (
            select(CoffeeOrm)
            .order_by(CoffeeOrm.id)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        query_result = await self.session.execute(query)
        return query_result.scalars().all()

    async def get_by_id(self, *, coffee_id: int) -> CoffeeOrm | None:
        """Get Coffee by id"""
        coffee = await self.session.get(CoffeeOrm, coffee_id)
        return coffee

    async def get_by_category(self, *, category: CoffeeCategory, pagination: Paginator) -> list[CoffeeOrm]:
        """Get Coffee by category"""
        query = (
            select(CoffeeOrm)
            .where(CoffeeOrm.category == category)
            .order_by(CoffeeOrm.id)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        query_result = await self.session.execute(query)
        return query_result.scalars().all()

    async def create(self, *, new_coffee: CreateCoffee) -> CoffeeOrm | None:
        """Create new Coffee object"""
        coffee = CoffeeOrm(**new_coffee.model_dump())
        self.session.add(coffee)
        await self.session.commit()
        await self.session.refresh(coffee)
        return coffee

    async def update(self, *, coffee: CoffeeOrm, update_data: UpdateCoffee) -> CoffeeOrm:
        """Update coffee"""
        coffee.title = update_data.title
        coffee.description = update_data.description
        coffee.price = update_data.price
        coffee.category = update_data.category
        coffee.size = update_data.size
        coffee.image_url = update_data.image_url

        await self.session.commit()
        await self.session.refresh(coffee)
        return coffee

    async def update_partial(self, *, coffee: CoffeeOrm, update_data: UpdateCoffeePartial) -> CoffeeOrm:
        """Update partial coffee"""
        if update_data.title:
            coffee.title = update_data.title

        if update_data.description:
            coffee.description = update_data.description

        if update_data.price:
            coffee.price = update_data.price

        if update_data.category:
            coffee.category = update_data.category

        if update_data.size:
            coffee.size = update_data.size

        if update_data.image_url:
            coffee.image_url = update_data.image_url

        await self.session.commit()
        await self.session.refresh(coffee)
        return coffee

    async def delete(self, *, coffee: CoffeeOrm):
        """Delete Coffee object"""
        await self.session.delete(coffee)
        await self.session.commit()
