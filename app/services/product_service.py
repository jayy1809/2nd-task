from fastapi import HTTPException, Depends, Response
from fastapi.responses import JSONResponse, StreamingResponse
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.utils.get_data_from_api import get_json_from_api
from app.utils.pdf_generator import generate_pdf
from app.config.settings import settings
from app.models.domain.product import Product
from app.models.schemas.product_schema import ProductCreate
import random

class ProductService():
    def __init__(self, product_repository: ProductRepository = Depends(ProductRepository), user_repository: UserRepository = Depends(UserRepository)):
        self.product_repository = product_repository
        self.user_repository = user_repository
    
    async def create_product(self, product_data: ProductCreate):
        product = Product(**product_data.model_dump())
        product_id = await self.product_repository.create_product(product)
        new_product = await self.product_repository.get_product_by_id(product_id)
        return new_product
    
    async def preload_data(self):
        api_response = await get_json_from_api(settings.PRODUCT_FETCH_API)
        parsed_products = []
        response_products = []
        products = api_response.get("products", [])

        seller_ids = await self.user_repository.get_role_user_ids("seller")
        if not seller_ids:
            return JSONResponse(
                status_code=404,
                content={
                    "data": [],
                    "status": 404,
                    "detail": "No sellers found in the database",
                    "error": "NoSellerIDsError: No seller IDs were found in the database."
                }
            )

        for product in products:
            parsed_product = {
                "title": product.get("title"),
                "description": product.get("description"),
                "category": product.get("category"),
                "price": product.get("price"),
                "rating": product.get("rating"),
                "brand": product.get("brand"),
                "images": product.get("images", []),  # Default to empty list if images are missing
                "seller_id": random.choice(seller_ids),
                "thumbnail": product.get("thumbnail")
                
            }
            parsed_products.append(parsed_product)
        
        for product in parsed_products:
            product = Product(**product)
            await self.product_repository.create_product(product)
            response_products.append(product.to_dict())
        
        return response_products
        # return parsed_products

    async def get_products(self):
        products = await self.product_repository.get_products()
        return products
    
    async def get_product_by_id(self, product_id: str):
        product = await self.product_repository.get_product_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )
        return product
    
    async def update_product(self, product_id: str, seller_id: str, product_update_data: dict):
        product = await self.product_repository.get_product_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )
        
        if product.get("seller_id") != seller_id:
            raise HTTPException(
                status_code=403,
                detail="Unauthorized, you are not the seller of the product"
            )
        
        updated_product = await self.product_repository.update_product(product_id, product_update_data)
        return updated_product
    


    async def delete_product(self, product_id: str, seller_id: str):
        product = await self.product_repository.get_product_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )
        
        if product.get("seller_id") != seller_id:
            raise HTTPException(
                status_code=403,
                detail="Unauthorized, you are not the seller of the product"
            )
        
        result = await self.product_repository.delete_product(product_id)
        return result
    


    async def download_product(self, product_id: str):
        product = await self.product_repository.get_product_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )
        
        pdf = generate_pdf(product)

        return StreamingResponse(
            iter([pdf]),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={product.get('title')}.pdf"}
        )
        
        
    