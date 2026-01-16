from sqlalchemy.orm import sessionmaker
from db.utils.db_engine import engine

Session = sessionmaker(bind=engine)


def dbSession():
    session = Session()
    try:
        yield session
    finally:
        session.close()
