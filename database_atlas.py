import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from typing import Optional
import logging
from bson import ObjectId

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database = None

mongodb = MongoDB()

async def connect_to_mongodb():
    """Create MongoDB Atlas connection"""
    try:
        # Get MongoDB URL from environment variable
        mongodb_url = os.getenv("MONGODB_URL")
        if not mongodb_url:
            raise Exception("MONGODB_URL environment variable is required")
        
        database_name = os.getenv("DATABASE_NAME", "ecommerce")
        
        logger.info("Connecting to MongoDB Atlas...")
        
        # Create client for Atlas connection
        mongodb.client = AsyncIOMotorClient(
            mongodb_url,
            server_api=ServerApi('1'),
            retryWrites=True,
            w='majority'
        )
        
        # Get database
        mongodb.database = mongodb.client[database_name]
        
        # Test the connection
        await mongodb.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB Atlas!")
        
        # Create indexes for better performance
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Error connecting to MongoDB Atlas: {e}")
        raise

async def close_mongodb_connection():
    """Close database connection"""
    if mongodb.client:
        mongodb.client.close()
        logger.info("MongoDB connection closed")

async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # Index on product name for faster text searches
        await mongodb.database.products.create_index("name")
        
        # Index on user ID for faster order queries
        await mongodb.database.orders.create_index("userId")
        
        # Text index for product search
        await mongodb.database.products.create_index([("name", "text")])
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.warning(f"Could not create indexes: {e}")

def get_database():
    """Get database instance"""
    if mongodb.database is None:
        raise Exception("Database not connected. Call connect_to_mongodb() first.")
    return mongodb.database

# Health check function
async def check_database_health():
    """Check if database is healthy"""
    try:
        if mongodb.client:
            await mongodb.client.admin.command('ping')
            return {"status": "healthy", "database": "mongodb_atlas"}
        else:
            return {"status": "disconnected", "database": "mongodb_atlas"}
    except Exception as e:
        return {"status": "error", "database": "mongodb_atlas", "error": str(e)}