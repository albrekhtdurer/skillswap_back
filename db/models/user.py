from datetime import datetime

from sqlalchemy import desc, select
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Класс для представления Пользователя в БД

    Attributes:
        id(int): id пользователя
        name(str): имя пользователя
        email(str): email пользователя
        password(str): пароль пользователя
        location(str): название города, в котором находится пользователь
        likes(int): количество лайков у пользователя
        birthDate(datetime): дата рождения
        createdAt(datetime): дата создания записи о пользователе
        userDescription(str): описание пользователя (раздел "о себе")
        avatar(str): путь к файлу с аватаром пользователя на сервере
        gender(str): пол пользователя
        skillCanTeachDescription(str): описание навыка, которому может научить пользователь
        skillCanTeachId(int): id навыка, которому может научить пользователь
        subcategoriesToLearn(str): JSON со списком id подкатегорий, которм хочет научиться пользователь

    Methods:
        create(cls, data, session): Метод добавления новой записи Пользователя в БД
        get(cls, id, session): Метод получения Пользователя из БД по его id
        getByEmail(cls, email, session): Метод получения Пользователя из БД по его email
        getPart(cls, offset, limit, session): Метод получения части записей Пользователей из БД
        getNew(cls, limit, session): Метод получения пользователей с наибольшим createdAt из БД (самых новых)
        getPopular(cls, limit, session): Метод получения пользователей с наибольшим likes из БД (самых популярных)
        update(self, data, session): Метод обновления данных пользователя в БД
    """

    id: int = Field(primary_key=True)
    name: str = Field()
    email: str = Field(nullable=True)
    password: str = Field(nullable=True, max_length=256)
    location: str = Field()
    likes: int = Field()
    birthDate: datetime = Field()
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    userDescription: str = Field()
    avatar: str = Field()
    gender: str = Field()
    skillCanTeachDescription: str = Field()
    skillCanTeachId: int = Field(foreign_key="skill.id")

    subcategoriesToLearn: str = Field()
    favourites: str = Field(nullable=True)

    @classmethod
    def create(cls, data, session):
        """Метод добавления новой записи Пользователя в БД

        Args:
            data (dict): словарь с данными пользователя.
            session (Session): сессия для подключения к БД.

        Returns:
            User: созданный экземпляр класса Пользователя
        """
        newUser = cls(
            name=data.get("name", ""),
            email=data.get("email", ""),
            password=data.get("password", ""),
            location=data.get("location", ""),
            likes=data.get("likes", 0),
            birthDate=data.get("birthDate"),
            userDescription=data.get("userDescription", ""),
            avatar=data.get("avatar", ""),
            gender=data.get("gender", ""),
            skillCanTeachDescription=data.get("skillCanTeachDescription", ""),
            skillCanTeachId=data.get("skillCanTeachId"),
            subcategoriesToLearn=data.get("subcategoriesToLearn", ""),
            favourites=data.get("favourites", ""),
            createdAt=data.get("createdAt"),
        )
        session.add(newUser)
        session.commit()
        return newUser

    @classmethod
    def get(cls, id, session):
        """Метод получения Пользователя из БД по его id

        Args:
            id (int): id Пользователя
            session (Session): сессия для подключения к БД.

        Returns:
            User: найденный экземпляр класса Пользователя
        """
        stmt = select(cls).where(cls.id == id)
        user = session.execute(stmt).scalars().first()
        return user

    @classmethod
    def getByEmail(cls, email, session):
        """Метод получения Пользователя из БД по его email

        Args:
            email (str): email Пользователя
            session (Session): сессия для подключения к БД.

        Returns:
            User: найденный экземпляр класса Пользователя
        """

        stmt = select(cls).where(cls.email == email)
        user = session.execute(stmt).scalars().first()
        return user

    @classmethod
    def getPart(cls, offset, limit, session):
        """Метод получения части записей Пользователей из БД

        Args:
            offset (int): Показатель смещения для пагинации.
            limit (int): Лимит выгрузки пользователей за один запрос.
            session (Session): сессия для подключения к БД.

        Returns:
            List[User]: список найденных экземпляров класса Пользователя
        """
        stmt = select(cls).order_by(cls.id).limit(limit).offset(offset)
        users = session.execute(stmt).scalars().all()
        return users

    @classmethod
    def getNew(cls, limit, session):
        """Метод получения пользователей с наибольшим createdAt из БД (самых новых)

        Args:
            limit (int): Количество пользователей, данные которых нужно получить.
            session (Session): сессия для подключения к БД.

        Returns:
            List[User]: список найденных экземпляров класса Пользователя
        """
        stmt = select(cls).order_by(desc(cls.createdAt)).limit(limit)
        users = session.execute(stmt).scalars().all()
        return users

    @classmethod
    def getPopular(cls, limit, session):
        """Метод получения пользователей с наибольшим likes из БД (самых популярных)

        Args:
            limit (int): Количество пользователей, данные которых нужно получить.
            session (Session): сессия для подключения к БД.

        Returns:
            List[User]: список найденных экземпляров класса Пользователя
        """
        stmt = select(cls).order_by(desc(cls.likes)).limit(limit)
        users = session.execute(stmt).scalars().all()
        return users

    def update(self, data, session):
        """Метод обновления данных пользователя в БД

        Args:
            data (dict): словарь с данными, которые нужно обновить
            session (Session): сессия для подключения к БД.

        Returns:
            User: экземпляр класса Пользователя с обновленными полями
        """
        for key, value in data.items():
            self.__setattr__(key, value)
        session.add(self)
        session.commit()
        return self
