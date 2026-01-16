from datetime import datetime
from pydantic import BaseModel
from typing import Dict, List, Optional, Any


class RegisterUserInfo(BaseModel):
    """Класс для представления модели данных Информации о пользователе при регистрации

    Attributes:
        email(str): email пользователя
        password(str): пароль пользователя
        name(str): имя пользователя
        birthDate(str): дата рождения
        location(str): название города, в котором находится пользователь
        gender(str): пол пользователя
        categoryWantToLearn(list[int]): список id категорий, навыкам которых хочет научиться пользователь
        subcategoryWantToLearn(list[int]): список id подкатегорий, навыкам которых хочет научиться пользователь
        skillCanTeach(dict): словарь с информацией о навыке, которому может научить пользователь
    """

    email: str
    password: str
    name: str
    birthDate: str
    location: str
    gender: str
    categoryWantToLearn: List[int]
    subcategoryWantToLearn: List[int]
    skillCanTeach: dict


class UpdateUserInfo(BaseModel):
    """Класс для представления модели данных Информации о пользователе при обновлении данных

    Attributes:
        email(str, optional): email пользователя
        name(str, optional): имя пользователя
        birthDate(str, optional): дата рождения
        location(str, optional): название города, в котором находится пользователь
        gender(str, optional): пол пользователя
        userDescription(str, optional): описание пользователя (раздел "о себе")
    """

    email: Optional[str]
    name: Optional[str]
    birthDate: Optional[str]
    location: Optional[str]
    gender: Optional[str]
    userDescription: Optional[str]


class UserInfo(BaseModel):
    """Класс для представления модели данных Информации о пользователе (для ответа сервера со списком пользователей)

    Attributes:
        id(int): id пользователя
        name(str): имя пользователя
        location(str): название города, в котором находится пользователь
        likes(int): количество лайков у пользователя
        isLiked(bool): лайкнут ли пользователь текущим юзером
        createdAt(str): дата создания карточки пользователя
        description(str): описание пользователя
        avatarUrl(str): ссылка для получения аватара пользователя
        skillCanTeach(dict[str, any]): информация о навыке, которому может научить пользователь
        subcategoriesWantToLearn(list[dict[str, any]]): информация о подкатегориях, навыкам из которых хочет научиться 
        пользователь
        gender(str): пол пользователя
        images(list[str]): список ссылок для получения картинок пользователя
    """
    id: int
    name: str
    location: str
    likes: int
    isLiked: bool
    age: str
    createdAt: datetime
    description: str
    avatarUrl: str
    skillCanTeach: Dict[str, Any]
    subcategoriesWantToLearn: List[Dict[str, Any]]
    gender: str
    images: List[str]

class CurrentUserInfo(BaseModel):
    """Класс для представления модели данных Информации о пользователе (для текущего пользователя)

    Attributes:
        id(int): id пользователя
        name(str): имя пользователя
        email(str): email пользователя
        location(str): название города, в котором находится пользователь
        description(str): описание пользователя
        avatarUrl(str): ссылка для получения аватара пользователя
        gender(str): пол пользователя
        birthDate(str): дата рождения пользователя
    """
    id: int
    name: str
    email: str
    location: str
    gender: str
    avatarUrl: str
    description: str
    birthDate: str
