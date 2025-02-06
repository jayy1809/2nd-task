from fastapi import Response, Depends
from app.usecases.cart_usecase import CartUseCase
from app.models.schemas.cart_schema import CartItem


class CartController:
    def __init__(self, cart_usecase: CartUseCase = Depends(CartUseCase)):
        self.cart_usecase = cart_usecase
    
    async def add_to_cart(self, user_id: str, cart_item: CartItem):
        return await self.cart_usecase.add_to_cart(user_id, cart_item)
    
    async def remove_from_cart(self, user_id: str, product_id: str):
        return await self.cart_usecase.remove_from_cart(user_id, product_id)
    
    async def get_cart(self, user_id: str):
        return await self.cart_usecase.get_cart(user_id)