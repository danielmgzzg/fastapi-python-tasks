from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from .settings import api_settings as settings

client = MongoClient(settings.uri, settings.port)
db: Database = client[settings.database]
collection: Collection = db[settings.collection]
