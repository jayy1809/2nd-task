from app.repositories.cart_repository import CartRepository
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository
from fastapi import Depends, HTTPException
from app.models.schemas.order_schema import OrderItem, Order
from app.models.domain.order import OrderItem as DomainOrderItem, Order as DomainOrder

class OrderService:
    def __init__(self, cart_repository: CartRepository = Depends(CartRepository),
                 user_repository: UserRepository = Depends(UserRepository),
                 product_repository: ProductRepository = Depends(ProductRepository),
                 order_repository: OrderRepository = Depends(OrderRepository)):
        self.cart_repository = cart_repository
        self.user_repository = user_repository
        self.product_repository = product_repository
        self.order_repository = order_repository
    
    async def create_order(self, user_id: str):
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Unable to find user, please login again")
        
        cart_items = await self.cart_repository.get_cart(user_id)
        if not cart_items:
            raise HTTPException(status_code=404, detail="could not find Cart for user")
        
        order_items = []
        for cart_item in cart_items:
            product = await self.product_repository.get_product_by_id(cart_item["product_id"])
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            order_item = DomainOrderItem(product_id=product["_id"], quantity=cart_item["quantity"], price=product["price"])
            order_items.append(order_item)
        
        order = DomainOrder(user_id=user["_id"], items=order_items, order_status="delivered")
        return await self.order_repository.create_order(order)
    
    async def get_order_history(self, user_id: str):
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Unable to find user, please login again")
        
        try:
            return await self.order_repository.get_order_by_user_id(user_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_order_by_id(self, user_id: str, order_id: str):
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Unable to find user, please login again")
        
        try:
            return await self.order_repository.get_order_by_id(user_id, order_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))