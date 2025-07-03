from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import MONGODB_URL, DB_NAME

class Database:

    def __init__(self):
        self.client = AsyncIOMotorClient(MONGODB_URL)
        self.db = self.client[DB_NAME]

    async def connect_to_mongo(self):
        """Connect to MongoDB"""
        self.client = AsyncIOMotorClient(MONGODB_URL)
        self.db = self.client[DB_NAME]
        print(f"Connected to MongoDB at {MONGODB_URL}")

    def close_mongo_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("Closed MongoDB connection")

db = Database()

def get_database():
    """Get database instance"""
    return db.db 