import json
import os
import random
import string
from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from api.login import manager
from config import config
from db.models.images import Image
from db.models.skill import Skill
from db.models.user import User
from db.utils.db_session import dbSession
from utils.hash_pwd import pwd_context
from models.response import BaseResponse, CurrentUserResponse
from models.user import RegisterUserInfo, UpdateUserInfo
from utils.prepare_current_user_data import prepare_current_user_data

router = APIRouter(prefix="/user", redirect_slashes=False)


@router.post("/", response_model=CurrentUserResponse)
async def registerUser(payload: RegisterUserInfo) -> CurrentUserResponse:
    """Метод для регистрации нового пользователя.

    Args:
        payload (RegisterUserInfo): Словарь с данными пользователя для регистрации

    Raises:
        HTTPException: 400 ошибка в случае, если пользователь с указанным email уже существует

    Returns:
        CurrentUserResponse: Класс ответа с данными о текущем пользователе
    """
    session = next(dbSession())
    existingUser = User.getByEmail(payload.email, session)
    if existingUser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже зарегистрирован!",
        )
    skill = Skill.getByName(payload.skillCanTeach["name"], session)
    if not skill:
        skill = Skill.create(payload.skillCanTeach, session)
    data = {
        "name": payload.name,
        "location": payload.location,
        "birthDate": datetime.strptime(payload.birthDate, "%Y-%m-%dT%H:%M:%S.%fZ"),
        "userDescription": "Напишите пару строк о себе",
        "gender": payload.gender,
        "skillCanTeachId": skill.id,
        "skillCanTeachDescription": payload.skillCanTeach["description"],
        "subcategoriesToLearn": json.dumps(payload.subcategoryWantToLearn),
        "email": payload.email,
        "password": pwd_context.hash(payload.password),
        "avatar": "no avatar",
    }
    newUser = User.create(data, session)
    access_token = manager.create_access_token(
        data={"sub": newUser.email}, expires=timedelta(days=3)
    )
    userData = prepare_current_user_data(newUser)
    session.close()
    return {
        "status": 200,
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "user": userData,
        },
    }


@router.get("/", response_model=BaseResponse)
async def getUser(user=Depends(manager)) -> BaseResponse:
    """Метод для получения данных текущего пользователя при наличии токена
    авторизации.

    Args:
        user (User, optional): экземпляр класса User с данными текущего пользователя. Получается по токену авторизации

    Returns:
        BaseResponse: Базовый класс ответа. В поле data - словарь с одним ключом user и словарем с данными 
        пользователя в качестве значения
    """
    return {"status": 200, "data": {"user": prepare_current_user_data(user)}}


@router.patch("/", response_model=BaseResponse)
async def updateUser(payload: UpdateUserInfo, user=Depends(manager)) -> BaseResponse:
    """Метод для обновления данных пользователя.

    Args:
        payload (UpdateUserInfo): Словарь с данными пользователя для обновления
        user (User, optional): экземпляр класса User с данными текущего пользователя. Получается по токену авторизации

    Returns:
        BaseResponse: Базовый класс ответа. В поле data - словарь с одним ключом user и словарем с данными 
        пользователя в качестве значения
    """
    data = payload.model_dump(exclude_none=True)
    updateUserSession = next(dbSession())
    if "birthDate" in data:
        data["birthDate"] = datetime.strptime(
            data["birthDate"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
    updatedUser = user.update(data, updateUserSession)
    userData = prepare_current_user_data(updatedUser)
    updateUserSession.close()
    return BaseResponse(status=200, data={"user": userData})


@router.post("/{id}/avatar", response_model=BaseResponse)
async def addAvatar(id: int, file: UploadFile = File(...)) -> BaseResponse:
    """Метод для добавления аватара пользователя.

    Args:
        id (int): id пользователя, которому добавляем аватар
        file (UploadFile, optional): Файл с аватаром.

    Returns:
        BaseResponse: Базовый класс ответа. В поле data - словарь с одним ключом "avatar" и путем для получения 
        аватара в качестве значения.
    """
    contents = await file.read()
    avatarSession = next(dbSession())
    if not os.path.exists(f"/opt/uploaded_files/avatars/{id}"):
        os.mkdir(f"/opt/uploaded_files/avatars/{id}")
    with open(f"/opt/uploaded_files/avatars/{id}/{file.filename}", "wb") as f:
        f.write(contents)
    currentUser = User.get(id, avatarSession)
    avatar_path = (
        "http://" + config.host + ":" + config.port + f"/api/v1/user/{id}/avatar/1"
    )
    currentUser.update({"avatar": avatar_path}, session=avatarSession)
    avatarSession.close()
    return BaseResponse(status=200, data={"avatar": avatar_path})


@router.get("/{id}/avatar/{hashed_filename}", response_model=BaseResponse)
async def getAvatar(id: int, hashed_filename: str) -> BaseResponse:
    """Метод получения аватара пользователя.

    Args:
        id (int): id пользователя, для которого получаем аватар
        hashed_filename (str): имя файла с аватаром

    Returns:
        FileResponse: Класс ответа с файлом.
    """
    filename = os.listdir(f"/opt/uploaded_files/avatars/{id}")[0]
    ext = filename.split(".")[-1]
    return FileResponse(
        f"/opt/uploaded_files/avatars/{id}/{filename}",
        filename=filename,
        media_type=f"image/{ext}",
    )


@router.patch("/{id}/avatar", response_model=BaseResponse)
async def updateAvatar(id: int, file: UploadFile = File(...)) -> BaseResponse:
    """Метод обновления аватара пользователя.

    Args:
        id (int): id пользователя, которому добавляем аватар
        file (UploadFile, optional): Файл с аватаром.

    Returns:
        BaseResponse: Базовый класс ответа. В поле data - словарь с одним ключом "avatar" и путем для получения 
        аватара в качестве значения.
    """
    contents = await file.read()
    avatar_folder_path = f"/opt/uploaded_files/avatars/{id}"
    if os.path.exists(avatar_folder_path):
        for filename in os.listdir(avatar_folder_path):
            file_path = os.path.join(avatar_folder_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
    else:
        os.mkdir(avatar_folder_path)
    with open(f"{avatar_folder_path}/{file.filename}", "wb") as f:
        f.write(contents)
    hashed_filename = "".join(random.choices(string.digits, k=12))
    avatar_path = (
        "http://"
        + config.host
        + ":"
        + config.port
        + f"/api/v1/user/{id}/avatar/{hashed_filename}"
    )
    avatarUpdateSession = next(dbSession())
    currentUser = User.get(id, avatarUpdateSession)
    currentUser.update({"avatar": avatar_path}, session=avatarUpdateSession)
    avatarUpdateSession.close()
    return BaseResponse(status=200, data={"avatar": avatar_path})


@router.post("/{id}/images", response_model=BaseResponse)
async def addImages(id: int, files: List[UploadFile] = []) -> BaseResponse:
    """Метод добавления картинок для определенного пользователя.

    Args:
        id (int): id пользователя, для которого добавляем картинки
        files (List[UploadFile], optional): Список файлов с картинками, которые хотим загрузить. По умолчанию пустой.

    Returns:
        BaseResponse: Базовый класс ответа, не имеет поля data.
    """
    imagesSession = next(dbSession())
    if not os.path.exists(f"/opt/uploaded_files/images/{id}"):
        os.mkdir(f"/opt/uploaded_files/images/{id}")
    for file in files:
        contents = await file.read()
        with open(f"/opt/uploaded_files/images/{id}/{file.filename}", "wb") as f:
            f.write(contents)
        Image.create(
            userId=id,
            session=imagesSession,
            path="http://"
            + config.host
            + ":"
            + config.port
            + f"/api/v1/user/{id}/images/{file.filename}",
        )
    imagesSession.close()
    return BaseResponse(status=200)


@router.get("/{id}/images/{filename}", response_model=BaseResponse)
async def getImage(id: int, filename: str) -> BaseResponse:
    """Метод получения картинки.

    Args:
        id (int): id пользователя, который загружал картинку
        filename (str): имя файла с картинкой

    Returns:
        BaseResponse: Базовый класс ответа.
    """
    ext = filename.split(".")[-1]
    return FileResponse(
        f"/opt/uploaded_files/images/{id}/{filename}",
        filename=filename,
        media_type=f"image/{ext}",
    )
