from app.repositories.cart_repository import CartRepository
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.complaint_repository import ComplaintRepository
from app.models.schemas.complaint_schema import ComplaintCreate
from app.models.domain.complaint import Complaint
from fastapi import Depends, HTTPException
from app.models.schemas.cart_schema import CartItem
from app.models.domain.cart import Cart

class ComplaintService:
    def __init__(self, cart_repository: CartRepository = Depends(CartRepository),
                 user_repository: UserRepository = Depends(UserRepository),
                 product_repository: ProductRepository = Depends(ProductRepository),
                 complaint_repository: ComplaintRepository = Depends(ComplaintRepository)
    ):
        self.product_repository = product_repository
        self.user_repository = user_repository
        self.cart_repository = cart_repository
        self.complaint_repository = complaint_repository

    
    async def create_complaint(self, complaint: ComplaintCreate):
        user_id = complaint.user_id

        user_dict = await self.user_repository.get_user_by_id(user_id)
        if user_dict is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        product_id = complaint.product_id
        product_dict = await self.product_repository.get_product_by_id(product_id)
        if product_dict is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        issue = complaint.issue
        image_url = complaint.image_url
        status = complaint.status
        
        complaint = Complaint(user_id=user_id, product_id=product_id, issue=issue, image_url=image_url, status=status)
        complaint_item = await self.complaint_repository.create_complaint(complaint)
        return complaint_item

