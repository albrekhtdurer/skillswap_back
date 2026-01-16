from sqlalchemy import select
from sqlmodel import Field, SQLModel


class Skill(SQLModel, table=True):
    """Класс для представления Навыка в БД

    Attributes:
        id(int): id навыка
        name(str): название навыка
        categoryId(int): id категории, к которой приндлежит навык
        subCategoryId(int): id подкатегории, к которой принадлежит навык

    Methods:
        create(cls, data, session): Метод добавления новой записи Навыка в БД
        get(cls, id, session): Метод получения Навыка из БД по его id
        getByName(cls, name, session): Метод получения Навыка из БД по его названию
    """

    id: int = Field(primary_key=True)
    name: str = Field()
    categoryId: int = Field(foreign_key="category.id")
    subCategoryId: int = Field(foreign_key="subcategory.id")

    @classmethod
    def create(cls, data, session):
        """Метод добавления новой записи Навыка в БД

        Args:
            data (dict): словарь с данными о Навыке. Должен содержать поля "name", "categoryId", "subcategoryId"
            session (Session): сессия для подключения к БД.

        Returns:
            Skill: созданный экземпляр класса Навыка
        """
        newSkill = cls(
            name=data.get("name", ""),
            categoryId=data.get("categoryId"),
            subCategoryId=data.get("subcategoryId"),
        )
        session.add(newSkill)
        session.commit()
        return newSkill

    @classmethod
    def get(cls, id, session):
        """Метод получения Навыка из БД по его id

        Args:
            id (int): id навыка
            session (Session): сессия для подключения к БД.

        Returns:
            Skill: найденный экземпляр класса Навыка
        """
        stmt = select(cls).where(cls.id == id)
        skill = session.execute(stmt).scalars().first()
        return skill

    @classmethod
    def getByName(cls, name, session):
        """Метод получения Навыка из БД по его названию

        Args:
            name(str): название навыка
            session (Session): сессия для подключения к БД.

        Returns:
            Skill: найденный экземпляр класса Навыка
        """
        stmt = select(cls).where(cls.name == name)
        skill = session.execute(stmt).scalars().first()
        return skill
