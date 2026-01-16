from sqlalchemy import select
from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    """Класс для представления Категории в БД

    Attributes:
        id(int): id категории
        name(str): название категории

    Methods:
        create(cls, data, session): Метод добавления новой записи категории в БД
        getAll(cls, session): Метод получения всех категорий из БД
    """

    id: int = Field(primary_key=True)
    name: str = Field()

    @classmethod
    def create(cls, data: dict, session):
        """Метод добавления новой записи категории в БД

        Args:
            data (dict): словарь с данными о категории. Должен содержать поле "name"
            session (Session): сессия для подключения к БД

        Returns:
            Category: созданный экземпляр класса Категории
        """
        newCategory = cls(name=data.get("name", ""))
        session.add(newCategory)
        session.commit()
        return newCategory

    @classmethod
    def getAll(cls, session):
        """Метод получения всех категорий из БД

        Args:
            session (Session): сессия для подключения к БД

        Returns:
            List[Category]: список с записями категорий в БД
        """
        stmt = select(cls)
        categories = session.execute(stmt).scalars().all()
        return categories
