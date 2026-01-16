# Вспомогательный скрипт для наполнения БД данными о навыках из мокового JSON пользователей
import json

from sqlalchemy.orm import sessionmaker

from db.models import Skill
from db_engine import engine

Session = sessionmaker(bind=engine)
session = Session()

with open("stat_data/users.json", "r") as file:
    users = json.load(file)

for user in users:
    data = user["skillCanTeach"]
    if Skill.getByName(data["name"], session):
        continue
    Skill.create(data, session)
