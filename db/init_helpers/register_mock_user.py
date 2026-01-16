# Вспомогательный скрипт для создания в БД нового пользователя с email/паролем
import json
from datetime import datetime


from sqlalchemy.orm import sessionmaker

from db.models import User
from db.models.skill import Skill
from db.utils.db_engine import engine
from utils.hash_pwd import pwd_context

Session = sessionmaker(bind=engine)
session = Session()

mockUserData = {
    "email": "albrekhtdurer@yandex.ru",
    "password": pwd_context.hash("EtoVasiliyKot"),
    "name": "Василий",
    "birthDate": datetime.strptime(
        "2020-03-09 12:00:00.127599", "%Y-%m-%d %H:%M:%S.%f"
    ),
    "location": "Москва",
    "gender": "male",
    "subcategoriesToLearn": json.dumps([{"id": 37, "name": "Питание и ЗОЖ"}]),
    "skillCanTeachDescription": "Научу вас виртуозно выпрашивать креветки, а также любые другие морепродукты и возможно мясо",
    "avatar": "http://localhost:8000/api/v1/user/46/avatar",
    "skillCanTeachId": 8,
}

mockSkillData = {
    "name": "Выпрашивание креветков",
    "categoryId": 1,
    "subCategoryId": 3,
}

Skill.create(mockSkillData, session)
User.create(mockUserData, session)
