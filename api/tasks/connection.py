from pymongo import MongoClient
from .settings import mongodb_uri, port

client = MongoClient(mongodb_uri, port)
db = client['usersdata']
