from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List, Dict, Optional
from datetime import datetime
from fastapi import HTTPException, Depends
from app.models.domain.product import Product
from app.config.database import get_database, Database

class ProductRepository:
    def __init__(self, database: AsyncIOMotorDatabase = Depends(get_database)):
        self.db = database
        self.collection = database.product_collection

    async def create_product(self, product: Product):
        """
        Create a new product in the database
        
        :param product_dict: Dictionary containing product details
        :return: Inserted product ID
        """
        try:
            product_dict = product.to_dict()
            result = await self.collection.insert_one(product_dict)
            return str(result.inserted_id)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error creating product: {str(e)}"
            )
    
    async def get_products(self) -> List[Dict]:
        try:
            products_cursor = self.collection.find()
            products = await products_cursor.to_list(length=None)
            return products
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error retrieving products: {str(e)}"
            )

    async def get_product_by_id(self, product_id: str) -> Optional[Dict]:
        """
        Retrieve a product by its ID
        
        :param product_id: String representation of product ObjectId
        :return: Product dictionary or None
        """
        try:
            product = await self.collection.find_one({"_id": product_id})
            return product
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"Product not found: {str(e)}"
            )

    async def update_product(self, product_id: str, update_data: Dict):
        """
        Update an existing product
        
        :param product_id: String representation of product ObjectId
        :param update_data: Dictionary of fields to update
        :return: Updated product details
        """
        try:
            # Remove _id if present in update_data to prevent modification error
            update_data.pop('_id', None)
            update_data.pop('seller_id', None)
            update_data.pop('created_at', None)
            
            update_data['updated_at'] = datetime.utcnow()

            result = await self.collection.update_one(
                {"_id": product_id},
                {"$set": update_data}
            )
            
            if result.modified_count == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found or no changes made"
                )
            
            return await self.get_product_by_id(product_id)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error updating product: {str(e)}"
            )

    async def delete_product(self, product_id: str):
        """
        Delete a product by its ID
        
        :param product_id: String representation of product ObjectId
        :return: Boolean indicating success of deletion
        """
        try:
            result = await self.collection.delete_one({"_id": product_id}) # if you wrap around in ObjectId() it will not work adn give error
            
            if result.deleted_count == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found"
                )
            
            return True
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error deleting product: {str(e)}"
            )

    async def get_products_by_category(self, category: str, skip: int = 0, limit: int = 10) -> List[Dict]:
        """
        Retrieve products by category with pagination
        
        :param category: Product category
        :param skip: Number of products to skip (for pagination)
        :param limit: Maximum number of products to return
        :return: List of product dictionaries
        """
        try:
            cursor = self.collection.find({"category": category}).skip(skip).limit(limit)
            products = await cursor.to_list(length=limit)
            return products
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error retrieving products by category: {str(e)}"
            )

    async def get_products_by_brand(self, brand: str, skip: int = 0, limit: int = 10) -> List[Dict]:
        """
        Retrieve products by brand with pagination
        
        :param brand: Product brand
        :param skip: Number of products to skip (for pagination)
        :param limit: Maximum number of products to return
        :return: List of product dictionaries
        """
        try:
            cursor = self.collection.find({"brand": brand}).skip(skip).limit(limit)
            products = await cursor.to_list(length=limit)
            return products
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error retrieving products by brand: {str(e)}"
            )

    async def search_products(self, query: str, skip: int = 0, limit: int = 10) -> List[Dict]:
        """
        Search products by title or description
        
        :param query: Search term
        :param skip: Number of products to skip (for pagination)
        :param limit: Maximum number of products to return
        :return: List of product dictionaries
        """
        try:
            search_filter = {
                "$or": [
                    {"title": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}}
                ]
            }
            cursor = self.collection.find(search_filter).skip(skip).limit(limit)
            products = await cursor.to_list(length=limit)
            return products
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error searching products: {str(e)}"
            )

    async def filter_products(self, 
                               min_price: Optional[float] = None, 
                               max_price: Optional[float] = None, 
                               min_rating: Optional[float] = None,
                               skip: int = 0, 
                               limit: int = 10) -> List[Dict]:
        """
        Filter products based on price range and minimum rating
        
        :param min_price: Minimum product price
        :param max_price: Maximum product price
        :param min_rating: Minimum product rating
        :param skip: Number of products to skip (for pagination)
        :param limit: Maximum number of products to return
        :return: List of product dictionaries
        """
        try:
            filter_query = {}
            
            if min_price is not None:
                filter_query["price"] = {"$gte": min_price}
            
            if max_price is not None:
                filter_query["price"] = filter_query.get("price", {})
                filter_query["price"]["$lte"] = max_price
            
            if min_rating is not None:
                filter_query["rating"] = {"$gte": min_rating}
            
            cursor = self.collection.find(filter_query).skip(skip).limit(limit)
            products = await cursor.to_list(length=limit)
            return products
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error filtering products: {str(e)}"
            )

    async def get_total_product_count(self, filter_query: Optional[Dict] = None) -> int:
        """
        Get total count of products, optionally with a filter
        
        :param filter_query: Optional filter to count specific products
        :return: Total number of products
        """
        try:
            filter_query = filter_query or {}
            return await self.collection.count_documents(filter_query)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error counting products: {str(e)}"
            )