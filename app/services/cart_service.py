from app.repositories.cart_repository import CartRepository
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from fastapi import Depends, HTTPException
from app.models.schemas.cart_schema import CartItem
from app.models.domain.cart import Cart

class CartService():
    def __init__(self, cart_repository: CartRepository = Depends(CartRepository),
                 user_repository: UserRepository = Depends(UserRepository),
                 product_repository: ProductRepository = Depends(ProductRepository)):
        
        self.product_repository = product_repository
        self.user_repository = user_repository
        self.cart_repository = cart_repository
    
    async def add_to_cart(self, user_id: str, cart_item: CartItem):
        user_dict = await self.user_repository.get_user_by_id(user_id)
        if user_dict is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        product_id = cart_item.product_id
        quantity = cart_item.quantity
        product_dict = await self.product_repository.get_product_by_id(product_id)
        if product_dict is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        cart = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        cart_item = await self.cart_repository.add_to_cart(cart)
        return cart_item
    
    async def remove_from_cart(self, user_id: str, product_id: str):
        user_dict = await self.user_repository.get_user_by_id(user_id)
        if user_dict is None:
            raise HTTPException(status_code=404, detail="User not found, provided invalid user id, validate user again by login in")
        
        # Proper way would be to go to cart and get dict of all the products that user has added to cart
        # and then check if the product_id is in the cart or not
        # but this is also better cause agar product collection mein nahi hai toh at the end buy b nahi kar payega buyer
        product_dict = await self.product_repository.get_product_by_id(product_id)
        if product_dict is None:
            raise HTTPException(status_code=404, detail="No such product found, provide proper product id")
        
        cart_item = await self.cart_repository.remove_from_cart(user_id, product_id)
        return cart_item
    
    async def get_cart(self, user_id: str):
        user_dict = await self.user_repository.get_user_by_id(user_id)
        if user_dict is None:
            raise HTTPException(status_code=404, detail="User not found, validate user again by login in")
        
        cart = await self.cart_repository.get_cart(user_id)
        return cart