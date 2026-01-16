from sqlalchemy import select
from sqlmodel import Field, SQLModel


class Subcategory(SQLModel, table=True):
    """Класс для представления Подкатегории в БД

    Attributes:
        id(int): id подкатегории
        name(str): название подкатегории
        categoryId(int): id категории, к которой принадлежит подкатегория

    Methods:
        create(cls, data, session): Метод добавления новой записи Подкатегории в БД
        get(cls, id, session): Метод получения Подкатегории из БД по ее id
        getAllByCategoryId(cls, id, session): Метод получения всех Подкатегорий из БД по id родительской категории
    """

    id: int = Field(primary_key=True)
    name: str = Field()
    categoryId: int = Field(foreign_key="category.id")

    @classmethod
    def create(cls, data, session):
        """Метод добавления новой записи Подкатегории в БД

        Args:
            data (dict): словарь с данными о Подкатегории. Должен содержать поля "name", "categoryId"
            session (Session): сессия для подключения к БД.

        Returns:
            Subcategory: созданный экземпляр класса Подкатегории
        """
        newSubCat = cls(name=data.get("name", ""), categoryId=data.get("categoryId"))
        session.add(newSubCat)
        session.commit()
        return newSubCat

    @classmethod
    def get(cls, id, session):
        """Метод получения Подкатегории из БД по ее id

        Args:
            id(int): id подкатегории
            session (Session): сессия для подключения к БД.

        Returns:
            Subcategory: найденный экземпляр класса Подкатегории
        """
        stmt = select(cls).where(cls.id == id)
        subcategory = session.execute(stmt).scalars().first()
        return subcategory

    @classmethod
    def getAllByCategoryId(cls, id, session):
        """Метод получения всех Подкатегорий из БД по id родительской категории

        Args:
            id (int): id категории, к которой принадлежит подкатегория
            session (Session): сессия для подключения к БД.

        Returns:
            List[Subcategory]: список найденных экземпляров класса Подкатегории
        """
        stmt = select(cls).where(cls.categoryId == id)
        subcategories = session.execute(stmt).scalars().all()
        return subcategories
