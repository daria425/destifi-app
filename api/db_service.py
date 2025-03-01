from db_connection import db_connection
from logger import logger

class DatabaseService:
    """Base class to manage MongoDB collection"""
    def __init__(self, collection_name:str):
        self.collection_name=collection_name
        self.collection=None
    async def init_collection(self):
        if db_connection.db is None:
            raise RuntimeError("Database connection is not initialized. Call `connect()` first.")
        self.collection=db_connection.db[self.collection_name]

class UserDatabaseService(DatabaseService):
    def __init__(self):
        super().__init__("users")

    async def login_user(self, user_data:dict):
        await self.init_collection()
        try:
            uid=user_data['uid']
            existing_user=await self.collection.find_one({"uid":uid}, {"_id":0})
            if existing_user:
                logger.info(f"Found existing user, returning data for {existing_user['uid']}")
                return existing_user
            inserted_doc=await self.collection.insert_one(user_data)
            logger.info(f"Successfully inserted user {inserted_doc.inserted_id}")
            del user_data['_id']
            return user_data
        except Exception as e:
            logger.error(f"Error occurred inserting user:{e}")