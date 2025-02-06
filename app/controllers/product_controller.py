from fastapi import Response, Depends
from app.usecases.product_usecase import ProductUseCase
from app.models.schemas.product_schema import ProductCreate


class ProductController():
    def __init__(self, product_usecase: ProductUseCase = Depends(ProductUseCase)):
        self.product_usecase = product_usecase

    async def preload_data(self):
        return await self.product_usecase.preload_data()
    
    async def get_products(self):
        return await self.product_usecase.get_products()
    
    async def get_product_by_id(self, product_id: str):
        return await self.product_usecase.get_product_by_id(product_id)
    
    async def update_product(self, product_id: str,seller_id: str,  product_update_data: dict):
        return await self.product_usecase.update_product(product_id, seller_id, product_update_data)

    async def delete_product(self, product_id: str, seller_id: str):
        return await self.product_usecase.delete_product(product_id, seller_id)
    
    async def download_product(self, product_id: str):
        return await self.product_usecase.download_product(product_id)
    
    async def create_product(self, product_data: ProductCreate):
        return await self.product_usecase.create_product(product_data)

    # async def get_all_products(self):
    #     return await self.product_usecase.get_all_products()

    # async def get_product_by_id(self, product_id: str):
    #     return await self.product_usecase.get_product_by_id(product_id)

    # async def create_product(self, product_data):
    #     return await self.product_usecase.create_product(product_data)

    # async def update_product(self, product_id: str, product_data):
    #     return await self.product_usecase.update_product(product_id, product_data)

    # async def delete_product(self, product_id: str):
    #     return await self.product_usecase.delete_product(product_id)