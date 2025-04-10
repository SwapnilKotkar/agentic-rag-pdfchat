from motor.motor_asyncio import AsyncIOMotorClient
from server.config import MONGO_URI
from server.config import DB_NAME

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]


def get_database():
    """Returns the MongoDB database instance."""
    return database
