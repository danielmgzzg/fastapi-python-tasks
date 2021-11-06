import os
from pydantic import (BaseSettings)


class Settings(BaseSettings):
    title: str = "Tasks API"
    port: int = os.environ["API_PORT"]
    uri: str = os.environ["MONGO_URI"]
    database: str = os.environ["MONGO_DB"]
    collection: str = "tasks"


api_settings = Settings()
