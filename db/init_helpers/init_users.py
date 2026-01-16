# Вспомогательный скрипт для наполнения БД данными о пользователях из мокового JSON
import json
from datetime import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import sessionmaker

from db.models import Image, User
from db_engine import engine

Session = sessionmaker(bind=engine)
session = Session()

with open("stat_data/users.json", "r") as file:
    users = json.load(file)

for user in users:
    age = int(user["age"].split()[0])
    birthDate = datetime.now() - relativedelta(years=age)
    print(birthDate)
    subcats = []
    for subcat in user["subcategoriesWantToLearn"]:
        subcats.append(subcat["id"])
    data = {
        "name": user["name"],
        "location": user["location"],
        "likes": user["likes"],
        "birthDate": birthDate,
        "createdAt": datetime.strptime(user["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"),
        "userDescription": user["description"],
        "avatar": user["avatarUrl"],
        "gender": user["gender"],
        "skillCanTeachDescription": user["skillCanTeach"]["fullDescription"],
        "skillCanTeachId": user["skillCanTeach"]["id"],
        "subcategoriesToLearn": json.dumps(subcats),
    }
    newUser = User.create(data, session)
    for image in user["images"]:
        Image.create(image, newUser.id, session)
