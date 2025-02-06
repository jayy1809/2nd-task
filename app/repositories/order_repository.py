from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from bson import ObjectId
from app.models.domain.order import Order
from app.config.database import get_database

class OrderRepository:
    def __init__(self, database: AsyncIOMotorDatabase = Depends(get_database)):
        self.db = database
        self.collection = database.order_collection

    async def create_order(self, order: Order):
        order_dict = order.to_dict()
        result = await self.collection.insert_one(order_dict)
        # response_return = {
        #     "order_id": str(result.inserted_id),
        #     "order": order_dict
        # }
        response_return = await self.collection.find_one({"_id": result.inserted_id})
        return response_return
    
    async def get_order_by_user_id(self, user_id: str):
        order = await self.collection.find({"user_id": user_id}).to_list(length=None)
        return order
    
    async def get_order_by_id(self, user_id: str, order_id: str):
        result = await self.collection.find_one({"_id": order_id, "user_id": user_id})
        return result