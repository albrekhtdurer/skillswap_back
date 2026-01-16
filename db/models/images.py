from sqlalchemy import select
from sqlmodel import Field, SQLModel


class Image(SQLModel, table=True):
    """Класс для представления Изображения в БД

    Attributes:
        id(int): id изображения
        path(str): путь к изображению на сервере
        userId(int): id пользователя, который загрузил изображение

    Methods:
        create(cls, path, userId, session): Метод добавления новой записи Изображения в БД
        getAllByUserId(cls, userId, session): Метод получения всех изображений для определенного пользователя
    """

    id: int = Field(primary_key=True)
    path: str = Field()
    userId: int = Field(foreign_key="user.id")

    @classmethod
    def create(cls, path, userId, session):
        """Метод добавления новой записи Изображения в БД

        Args:
            path (str): путь к изображению на сервере
            userId (str): id пользователя, который загрузил изображение
            session (Session): сессия для подключения к БД.

        Returns:
            Image: созданный экземпляр класса Изображения
        """
        newImage = cls(path=path, userId=userId)
        session.add(newImage)
        session.commit()
        return newImage

    @classmethod
    def getAllByUserId(cls, userId, session):
        """Метод получения всех изображений для определенного пользователя

        Args:
            userId (str): id пользователя, для которого получаем изображения
            session (Session): сессия для подключения к БД.

        Returns:
            List[Image]: список с экземплярами класса Изображения
        """
        stmt = select(cls).where(cls.userId == userId)
        images = session.execute(stmt).scalars().all()
        return images
