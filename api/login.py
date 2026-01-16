from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

from config import config
from db.models.user import User
from db_session import dbSession
from hash_pwd import pwd_context
from models.login import LoginInfo
from models.response import BaseResponse, CurrentUserResponse
from prepare_user_data import prepare_current_user_data

router = APIRouter(prefix="/auth")
secret = config.secret
manager = LoginManager(secret, token_url="/auth/login")


@manager.user_loader()
def load_user(email: str) -> User:
    """Коллбэк-метод для получения текущего юзера при отправке токена авторизации

    Args:
        email (str): email текущего пользователя

    Returns:
        User: экземпляр класса User с данными текущего пользователя
    """
    userSession = next(dbSession())
    user = User.getByEmail(email, userSession)
    userSession.close()
    return user


@router.post("/login", response_model=CurrentUserResponse)
async def login(payload: LoginInfo, session=Depends(dbSession)) -> CurrentUserResponse:
    """Метод для логина пользователя

    Args:
        payload (LoginInfo): Объект с данными для логина (email, пароль)
        session (Session, optional): сессия в БД.

    Raises:
        InvalidCredentialsException: Ошибка при невалидном email/пароле

    Returns:
        CurrentUserResponse: Класс ответа с данными о текущем пользователе
    """
    user = User.getByEmail(payload.email, session)
    if not user or not pwd_context.verify(payload.password, user.password):
        raise InvalidCredentialsException
    access_token = manager.create_access_token(
        data={"sub": user.email}, expires=timedelta(days=3)
    )
    userData = prepare_current_user_data(user)
    print("token  " + access_token)
    return {
        "status": 200,
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "user": userData,
        },
    }
