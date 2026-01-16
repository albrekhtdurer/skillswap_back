from pydantic import BaseModel


class Category(BaseModel):
    """Класс для представления модели данных Категории

    Attributes:
        id(int): id категории
        name(str): название категории
    """

    name: str
    id: int
