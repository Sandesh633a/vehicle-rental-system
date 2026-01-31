from flask_jwt_extended import JWTManager
from pymongo import MongoClient
import certifi

jwt = JWTManager()
mongo_client = None
db = None


def init_db(uri):
    """
    Initializes MongoDB connection with TLS support.
    Required for MongoDB Atlas + Render.
    """
    global mongo_client, db

    mongo_client = MongoClient(
        uri,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=30000
    )

    # Uses DB name from URI
    db = mongo_client.get_default_database()