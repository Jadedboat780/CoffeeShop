from fastapi import APIRouter, Path, Depends, status, HTTPException
from typing import Annotated

from app.db.models import CoffeeCategory
from app.endpoints.pagination import Paginator
from .crud import CoffeeDAO
from .schemas import GetCoffee, CreateCoffee, UpdateCoffee, UpdateCoffeePartial

router = APIRouter(prefix="/coffees", tags=["Coffees"])


@router.get("/{coffee_id}", status_code=status.HTTP_200_OK)
async def get_coffee(
        coffee_id: Annotated[int, Path(ge=1)],
        coffee_dao: CoffeeDAO = Depends()
):
    result = await coffee_dao.get_by_id(coffee_id=coffee_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Coffee {coffee_id} not found!")

    return result


@router.get("/", status_code=status.HTTP_200_OK)
async def get_coffees(
        pagination: Paginator = Depends(),
        coffee_dao: CoffeeDAO = Depends()
) -> list[GetCoffee]:
    coffees = await coffee_dao.get_partial(pagination=pagination)
    return [GetCoffee(**coffee.__dict__) for coffee in coffees]


@router.get("/category/{category}", status_code=status.HTTP_200_OK)
async def get_coffees_by_category(
        category: CoffeeCategory,
        pagination: Paginator = Depends(),
        coffee_dao: CoffeeDAO = Depends()
) -> list[GetCoffee]:
    coffees = await coffee_dao.get_by_category(category=category, pagination=pagination)
    return [GetCoffee(**coffee.__dict__) for coffee in coffees]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_coffee(
        coffee_data: CreateCoffee,
        coffee_dao: CoffeeDAO = Depends()
):
    coffee = await coffee_dao.create(new_coffee=coffee_data)
    return coffee


@router.put("/{coffee_id}", status_code=status.HTTP_201_CREATED)
async def update_coffee(
        coffee_id: Annotated[int, Path(ge=1)],
        update_data: UpdateCoffee,
        coffee_dao: CoffeeDAO = Depends()
) -> GetCoffee:
    coffee = await coffee_dao.get_by_id(coffee_id=coffee_id)
    if coffee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Coffee {coffee_id} not found!")

    coffee = await coffee_dao.update(coffee=coffee, update_data=update_data)
    return GetCoffee(**coffee.__dict__)


@router.patch("/{coffee_id}", status_code=status.HTTP_201_CREATED)
async def update_coffee_partial(
        coffee_id: Annotated[int, Path(ge=1)],
        update_data: UpdateCoffeePartial,
        coffee_dao: CoffeeDAO = Depends()
) -> GetCoffee:
    coffee = await coffee_dao.get_by_id(coffee_id=coffee_id)
    if coffee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Coffee {coffee_id} not found!")

    coffee = await coffee_dao.update_partial(coffee=coffee, update_data=update_data)
    return GetCoffee(**coffee.__dict__)


@router.delete("/{coffee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_coffee(
        coffee_id: Annotated[int, Path(ge=1)],
        coffee_dao: CoffeeDAO = Depends()
):
    coffee = await coffee_dao.get_by_id(coffee_id=coffee_id)
    if coffee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Coffee {coffee_id} not found!")

    await coffee_dao.delete(coffee=coffee)
