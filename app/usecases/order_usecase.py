from fastapi import HTTPException, status, Depends, Response
from app.services.order_service import OrderService
from app.models.schemas.order_schema import OrderItem, Order

class OrderUseCase:
    def __init__(self, order_service: OrderService = Depends(OrderService)):
        self.order_service = order_service
    
    async def create_order(self, user_id: str):
        return await self.order_service.create_order(user_id)
    
    async def get_order_history(self, user_id: str):
        return await self.order_service.get_order_history(user_id)
    
    async def get_order_by_id(self, user_id: str, order_id: str):
        return await self.order_service.get_order_by_id(user_id, order_id)