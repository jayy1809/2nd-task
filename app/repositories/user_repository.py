from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from bson import ObjectId
from app.models.domain.user import User  # Adjust the import path as necessary
# from app.db.mongodb import get_database  # Adjust the import path as necessary
from app.config.database import get_database, Database

class UserRepository:
    def __init__(self, database: AsyncIOMotorDatabase = Depends(get_database)): #get_database
        self.db = database
        self.collection = database.user_collection

    async def get_users(self):
        user_dicts = await self.collection.find().to_list(length=None)
        return user_dicts
    
    async def get_user_by_email(self, email: str):
        user_dict = await self.collection.find_one({"email": email})
        return user_dict

    async def get_user_by_id(self, user_id: str):
        user_dict = await self.collection.find_one({"_id": user_id})
        return user_dict

    async def create_user(self, user: User):
        user_dict = user.to_dict()
        result = await self.collection.insert_one(user_dict)
        return str(result.inserted_id)
    
    async def get_role_user_ids(self, role: str):
        user_dicts = await self.collection.find({"role": role}).to_list(length=None)
        user_ids = [str(user["_id"]) for user in user_dicts]
        return user_ids
    
    async def update_user_role(self, user_id: str, role: str):
        result = await self.collection.update_one({"_id": user_id}, {"$set": {"role": role}})
        return await self.get_user_by_id(user_id)