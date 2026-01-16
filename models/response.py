from pydantic import BaseModel
from typing import Dict, List, Optional, Any, TypedDict

from models.user import CurrentUserInfo, UserInfo


class BaseResponse(BaseModel):
    """Класс для представления модели данных базового ответа сервера

    Attributes:
        status(int): статус-код ответа
        data(dict, optional): словарь с дополнительными данными ответа
        error(string, optional): сообщение об ошибке
    """

    status: int
    data: Optional[Dict[str, Any]] = {}
    error: Optional[str] = ""

class UsersDict(BaseModel):
    users: List[UserInfo] = {}    

class UsersResponse(BaseResponse):
    """Класс для представления модели данных ответа сервера со списком пользователей

    Attributes:
        data(UsersDict): словарь с одним ключом "users" и списком со словарями данных пользователей в качестве значения.
    """    
    data: UsersDict

class CurrentUserDict(BaseModel):
    access_token: str
    token_type: str
    user: CurrentUserInfo

class CurrentUserResponse(BaseResponse):
    """Класс для представления модели данных ответа сервера с данными текущего пользователя

    Attributes:
        data(CurrentUserDict): словарь со следующими данными:
        "access_token": токен доступа,
        "token_type": "bearer",
        "user": словарь с данными текущего пользователя
    """    
    data: CurrentUserDict
