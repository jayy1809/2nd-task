from bson import ObjectId
from datetime import datetime
from typing import List, Optional   

class Complaint:
    def __init__(self, user_id: str, order_id: str, product_id: str, issue: str, image_url: Optional[str], status: Optional[str]):
        self._id = ObjectId()
        self.user_id = user_id
        self.order_id = order_id
        self.product_id = product_id
        self.issue = issue
        self.image_url = image_url
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "_id": str(self._id),
            "user_id": self.user_id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "issue": self.issue,
            "image_url": self.image_url,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
