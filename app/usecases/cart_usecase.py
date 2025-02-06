from fastapi import HTTPException, status, Depends, Response
from app.services.cart_service import CartService
from app.models.schemas.cart_schema import CartItem


class CartUseCase():
    def __init__(self, cart_service: CartService = Depends(CartService)):
        self.cart_service = cart_service
    
    async def add_to_cart(self, user_id: str, cart_item: CartItem):
        return await self.cart_service.add_to_cart(user_id, cart_item)
    
    async def remove_from_cart(self, user_id: str, product_id: str):
        return await self.cart_service.remove_from_cart(user_id, product_id)
    
    async def get_cart(self, user_id: str):
        return await self.cart_service.get_cart(user_id)