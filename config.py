from pydantic import BaseModel
import os


class Config(BaseModel):
    host: str = os.getenv("APP_HOST")
    port: str = os.getenv("APP_PORT")
    secret: str = os.getenv("APP_SECRET")


config = Config()
