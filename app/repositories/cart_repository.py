from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from bson import ObjectId
from app.models.domain.cart import Cart
from app.config.database import get_database

class CartRepository:

    def __init__(self, database: AsyncIOMotorDatabase = Depends(get_database)):
        self.db = database
        self.collection = database.cart_collection

    async def add_to_cart(self, cart: Cart):
        cart_dict = cart.to_dict()
        result = await self.collection.insert_one(cart_dict)
        return str(result.inserted_id)
    
    async def remove_from_cart(self, user_id: str, product_id: str):
        result = await self.collection.delete_one({"user_id": user_id, "product_id": product_id})
        
        if result.deleted_count == 0:
            raise Exception("No such Product found in cart")
        return result.deleted_count
    
    async def get_cart(self, user_id: str):
        cart = await self.collection.find({"user_id": user_id}).to_list(length=None)
        return cart