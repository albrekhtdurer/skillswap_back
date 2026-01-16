from fastapi import APIRouter

from db.models import City
from db.utils.db_session import dbSession
from models.response import BaseResponse

router = APIRouter(prefix="/cities", redirect_slashes=False)


@router.get("/all", response_model=BaseResponse)
async def getAllCities() -> BaseResponse:
    """Метод для получения всех городов.

    Returns:
        BaseResponse: Базовый класс ответа, в поле data - словарь с одним ключом "cities" и списком полученных 
        городов в качестве значения
    """
    citySession = next(dbSession())
    cities = City.getAll(citySession)
    cities_list = [{"id": city.id, "name": city.name} for city in cities]
    citySession.close()
    return BaseResponse(status=200, data={"cities": cities_list})
