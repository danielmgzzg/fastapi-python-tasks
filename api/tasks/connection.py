from pymongo import MongoClient
from .settings import api_settings as settings
from pymongo.collection import Collection
from pymongo.database import Database

client = MongoClient(settings.uri, settings.port)
db: Database = client[settings.database]
collection: Collection = db[settings.collection]
