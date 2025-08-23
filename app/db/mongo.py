from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None

async def connect_to_db() -> None:
    global _client, _db
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGODB_URI)
        _db = AsyncIOMotorDatabase(settings.MONGODB_DB)

async def close_mongo_connection() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None

#Expose db getter

def get_db() -> AsyncIOMotorDatabase:
    assert _db is not None, "MongoDB not initialized. Did you call connect_to_mongodb()?"
    return _db