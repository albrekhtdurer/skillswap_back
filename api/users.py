import json
from typing import List, Dict

from fastapi import APIRouter

from db.models import Image, Skill, Subcategory, User
from db.utils.db_session import dbSession
from models.response import UsersResponse
from models.user import UserInfo
from utils.prepare_full_user_data import prepare_full_user_data

router = APIRouter(prefix="/users", redirect_slashes=False)


def getDataAndPrepareUsers(users: List[User], session) -> List[UserInfo]:
    """Вспомогательная функция для преобразования данных пользователей из БД в данные для фронтенда

    Args:
        users (List[User]): список объектов пользователей из БД
        session (Session): сессия для подключения к БД

    Returns:
        List[Dict]: список словарей с данными пользователей
    """
    result = []
    for user in users:
        userSkill = Skill.get(user.skillCanTeachId, session=session)
        userSkill = {
            "id": userSkill.id,
            "name": userSkill.name,
            "categoryId": userSkill.categoryId,
            "subCategoryId": userSkill.subCategoryId,
            "fullDescription": user.skillCanTeachDescription,
        }
        subcatIds = json.loads(user.subcategoriesToLearn)
        userSubcats = []
        for id in subcatIds:
            subcategory = Subcategory.get(id, session=session)
            userSubcats.append({"id": subcategory.id, "name": subcategory.name})
        userImages = Image.getAllByUserId(user.id, session=session)
        result.append(
            prepare_full_user_data(
                user, skillCanTeach=userSkill, subcats=userSubcats, images=userImages
            )
        )
    return result


@router.get("/all", response_model=UsersResponse)
async def getAllUsers(offset: int = 0, limit: int = 150) -> UsersResponse:
    """Метод для получения всех пользователей

    Args:
        offset (int, optional): Показатель смещения для пагинации. По умолчанию 0.
        limit (int, optional): Лимит выгрузки пользователей за один запрос. По умолчанию 150.

    Returns:
        UsersResponse: Класс ответа со списком пользователей.
    """
    usersSession = next(dbSession())
    users = User.getPart(limit=limit, offset=limit * offset, session=usersSession)
    result = getDataAndPrepareUsers(users, usersSession)
    usersSession.close()
    return UsersResponse(status=200, data={"users": result})


@router.get("/new", response_model=UsersResponse)
async def getNewUsers(limit: int = 10) -> UsersResponse:
    """Метод для получения новых пользователей

    Args:
        limit (int, optional): Количество пользователей, данные которых нужно получить. По умолчанию 10.

    Returns:
        UsersResponse: Класс ответа со списком пользователей.
    """
    usersSession = next(dbSession())
    users = User.getNew(limit=limit, session=usersSession)
    result = getDataAndPrepareUsers(users, usersSession)
    usersSession.close()
    return UsersResponse(status=200, data={"users": result})


@router.get("/popular", response_model=UsersResponse)
async def getPopularUsers(limit: int = 10) -> UsersResponse:
    """Метод для получения популярных пользователей

    Args:
        limit (int, optional): Количество пользователей, данные которых нужно получить. По умолчанию 10.

    Returns:
        UsersResponse: Класс ответа со списком пользователей.
    """
    usersSession = next(dbSession())
    users = User.getPopular(limit=limit, session=usersSession)
    result = getDataAndPrepareUsers(users, usersSession)
    usersSession.close()
    return UsersResponse(status=200, data={"users": result})
