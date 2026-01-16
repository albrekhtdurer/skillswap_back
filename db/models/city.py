from sqlalchemy import select
from sqlmodel import Field, SQLModel


class City(SQLModel, table=True):
    """Класс для представления Города в БД

    Attributes:
        id(int): id города
        name(str): название города

    Methods:
        create(cls, data, session): Метод добавления новой записи города в БД
        getAll(cls, session): Метод получения всех городов из БД
    """

    id: int = Field(primary_key=True)
    name: str = Field()

    @classmethod
    def create(cls, data, session):
        """Метод добавления новой записи города в БД

        Args:
            data (dict): словарь с данными о городе. Должен содержать поле "name"
            session (Session): сессия для подключения к БД

        Returns:
            City: созданный экземпляр класса Города
        """
        newCity = cls(name=data.get("name", ""))
        session.add(newCity)
        session.commit()
        return newCity

    @classmethod
    def getAll(cls, session):
        """Метод получения всех городов из БД

        Args:
            session (Session): сессия для подключения к БД

        Returns:
            List[City]: список с записями городов в БД
        """
        stmt = select(cls)
        cities = session.execute(stmt).scalars().all()
        return cities
