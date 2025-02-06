from fastapi import HTTPException, status, Depends, Response
from app.services.product_service import ProductService  # Adjust the import path as necessary
from app.models.schemas.product_schema import ProductCreate

class ProductUseCase():
    def __init__(self, product_service: ProductService = Depends(ProductService)):
        self.product_service = product_service
    
    async def preload_data(self):
        result = await self.product_service.preload_data()
        return result
    
    async def get_products(self):
        return await self.product_service.get_products()
    
    async def get_product_by_id(self, product_id: str):
        return await self.product_service.get_product_by_id(product_id)
    
    async def update_product(self, product_id: str, seller_id: str, product_update_data: dict):
        return await self.product_service.update_product(product_id, seller_id, product_update_data)
    
    async def delete_product(self, product_id: str, seller_id: str):
        return await self.product_service.delete_product(product_id, seller_id)
    
    async def download_product(self, product_id: str):
        return await self.product_service.download_product(product_id)
    
    async def create_product(self, product_data: ProductCreate):
        return await self.product_service.create_product(product_data)