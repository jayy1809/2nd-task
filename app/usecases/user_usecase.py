from fastapi import HTTPException, status, Depends, Response
from app.services.user_service import UserService 
from app.models.schemas.user_schema import UserUpdate 

class UserUseCase():
    def __init__(self, user_service: UserService = Depends(UserService)):
        self.user_service = user_service
    
    async def get_users(self):
        return await self.user_service.get_users()
    
    async def get_user_by_id(self, user_id: str):
        user_dict = await self.user_service.get_user_by_id(user_id)
        return user_dict
    
    async def update_user_role(self, user_id: str, user_update: UserUpdate):
        return await self.user_service.update_user_role(user_id, user_update)