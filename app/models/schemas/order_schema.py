from pydantic import BaseModel, field_validator
from typing import Literal, List

class OrderItem(BaseModel): # ---> structure
    product_id: str
    quantity: int
    price: float

class Order(BaseModel): # ---> Schema
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: Literal["pending", "shipped", "delivered", "cancelled"]

    @field_validator('status')
    def validate_status(cls, v):
        valid_statuses = ['pending', 'shipped', 'delivered', 'cancelled']
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v
    
    @field_validator('user_id')
    async def validate_user_id(cls, v):
        if len(v) != 24:
            raise ValueError('provided invalid user id')
        return v

    @field_validator('total_amount')
    def validate_total_amount(cls, v):
        if v < 0:
            raise ValueError('Total amount cannot be negative')
        return v

