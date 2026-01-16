# Вспомогательный скрипт для наполнения БД данными о городах из мокового JSON
import json

from sqlalchemy.orm import sessionmaker

from db.models import City
from db.utils.db_engine import engine

Session = sessionmaker(bind=engine)
session = Session()

with open("stat_data/cities.json", "r") as file:
    cities = json.load(file)

for city in cities:
    cat = City.create(city, session)
