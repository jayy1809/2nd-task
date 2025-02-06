from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from fastapi import Depends, HTTPException
from app.models.schemas.user_schema import UserUpdate



class UserService():
    def __init__(self, product_repository: ProductRepository = Depends(ProductRepository), user_repository: UserRepository = Depends(UserRepository)):
        self.product_repository = product_repository
        self.user_repository = user_repository
    
    async def get_users(self):
        return await self.user_repository.get_users()
    
    async def get_user_by_id(self, user_id: str):
        user_dict = await self.user_repository.get_user_by_id(user_id)
        if user_dict is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user_dict
    
    async def update_user_role(self, user_id: str, user_update: UserUpdate):
        user_dict = await self.user_repository.get_user_by_id(user_id)
        if user_dict is None:
            raise HTTPException(status_code=404, detail="User not found")
        user_dict = await self.user_repository.update_user_role(user_id, user_update.role)
        return user_dict