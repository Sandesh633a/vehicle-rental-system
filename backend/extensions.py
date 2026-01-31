from flask_jwt_extended import JWTManager
from pymongo import MongoClient

jwt = JWTManager()
mongo_client = None
db = None

def init_db(uri):
    global mongo_client, db
    mongo_client = MongoClient(uri)
    db = mongo_client["vehicle_rental"]