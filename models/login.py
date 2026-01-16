from pydantic import BaseModel


class LoginInfo(BaseModel):
    """Класс для представления модели данных Информации о пользователе при логине

    Attributes:
        email(str): email пользователя
        password(str): пароль пользователя
    """

    email: str
    password: str


class LoginResponseModel(BaseModel):
    """Класс для представления модели данных ответа сервера при регистрации/логине пользователя

    Attributes:
        access_token(str): токен доступа
        token_type(str): тип токена доступа
        data(dict): словарь с данными пользователя
    """

    access_token: str
    token_type: str
    data: dict
