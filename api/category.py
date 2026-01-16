from fastapi import APIRouter

from db.models import Category, Subcategory
from db_session import dbSession
from models.response import BaseResponse

router = APIRouter(prefix="/categories", redirect_slashes=False)


@router.get("/all", response_model=BaseResponse)
async def getAllCategories() -> BaseResponse:
    """Метод для получения всех категорий

    Returns:
        BaseResponse: Базовый класс ответа, в поле data - словарь с одним ключом "categories" и списком полученных категорий в качестве значения
    """
    catSession = next(dbSession())
    categories = Category.getAll(catSession)
    categories_list = [
        {"id": category.id, "name": category.name} for category in categories
    ]
    ids = set([cat["id"] for cat in categories_list])
    for id in ids:
        subcats = Subcategory.getAllByCategoryId(id, catSession)
        categories_list[id - 1]["subcategories"] = [
            {"id": subcat.id, "name": subcat.name} for subcat in subcats
        ]
    catSession.close()
    return BaseResponse(status=200, data={"categories": categories_list})
