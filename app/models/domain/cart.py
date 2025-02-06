from bson import ObjectId
from datetime import datetime
from typing import List, Optional   



class Cart:
    def __init__(self, user_id: str, product_id: str, quantity: int):
        self._id = ObjectId()  
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.created_at = datetime.utcnow()  
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "_id": str(self._id), 
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat(),  
            "updated_at": self.updated_at.isoformat()
        }