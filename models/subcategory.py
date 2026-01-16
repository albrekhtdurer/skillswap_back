from pydantic import BaseModel


class Subcategory(BaseModel):
    """Класс для представления модели данных Подкатегории

    Attributes:
        id(int): id подкатегории
        name(str): название подкатегории
    """

    name: str
    id: int
