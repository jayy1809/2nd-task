from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from bson import ObjectId
from app.models.domain.complaint import Complaint
from app.config.database import get_database

class ComplaintRepository:
    
    def __init__(self, database: AsyncIOMotorDatabase = Depends(get_database)):
        self.db = database
        self.collection = database.complaint_collection

    async def create_complaint(self, complaint: Complaint):
        complaint_dict = complaint.to_dict()
        result = await self.collection.insert_one(complaint_dict)
        result_response = await self.collection.find_one({"_id": result.inserted_id})
        return result_response