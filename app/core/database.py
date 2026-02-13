"""Database connection and configuration"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

# Global variables for database connection
mongodb_client: AsyncIOMotorClient | None = None
mongodb_database: AsyncIOMotorDatabase | None = None


async def connect_to_mongo() -> None:
    """Establish connection to MongoDB"""
    global mongodb_client, mongodb_database
    
    mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    mongodb_database = mongodb_client[settings.MONGODB_DB_NAME]
    print(f"✓ Connected to MongoDB: {settings.MONGODB_DB_NAME}")


async def close_mongo_connection() -> None:
    """Close MongoDB connection"""
    global mongodb_client
    
    if mongodb_client:
        mongodb_client.close()
        print("✓ MongoDB connection closed")


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    if mongodb_database is None:
        raise RuntimeError("Database not initialized")
    return mongodb_database
