from bson import ObjectId
from datetime import datetime
from typing import List, Optional
from typing_extensions import Literal

class OrderItem:
    def __init__(self, product_id: str, quantity: int, price: float):
        self._id = ObjectId()
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.subtotal = price * quantity
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "_id": str(self._id),
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price": self.price,
            "subtotal": self.subtotal,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class Order:
    def __init__(
        self, 
        user_id: str, 
        items: List[OrderItem],
        order_status: Literal["pending", "shipped", "delivered", "cancelled"] = "pending"
    ):
        self._id = ObjectId()
        self.user_id = user_id
        self.items = items
        self.total_amount = sum(item.subtotal for item in items)
        self.order_status = order_status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        
    def to_dict(self):
        return {
            "_id": str(self._id),
            "user_id": self.user_id,
            "items": [item.to_dict() for item in self.items],
            "total_amount": self.total_amount,
            "order_status": self.order_status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    def update_status(self, status: str):
        self.order_status = status
        self.updated_at = datetime.utcnow()
