from fastapi import Response, Depends
from app.usecases.order_usecase import OrderUseCase
from app.models.schemas.order_schema import OrderItem, Order

class OrderController:
    def __init__(self, order_usecase: OrderUseCase = Depends(OrderUseCase)):
        self.order_usecase = order_usecase
    
    async def create_order(self, user_id: str):
        return await self.order_usecase.create_order(user_id)
    
    async def get_order_history(self, user_id: str):
        return await self.order_usecase.get_order_history(user_id)
    
    async def get_order_by_id(self, user_id: str, order_id: str):
        return await self.order_usecase.get_order_by_id(user_id, order_id)
