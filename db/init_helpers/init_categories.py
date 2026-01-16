# Вспомогательный скрипт для наполнения БД данными о категориях из мокового JSON
import json

from sqlalchemy.orm import sessionmaker

from db.models import Category, Subcategory
from db_engine import engine

Session = sessionmaker(bind=engine)
session = Session()

with open("stat_data/categories.json", "r") as file:
    categories = json.load(file)

for category in categories:
    cat = Category.create(category, session)
    for subcategory in category["subcategories"]:
        data = {"categoryId": cat.id, "name": subcategory["name"]}
        Subcategory.create(data, session)
