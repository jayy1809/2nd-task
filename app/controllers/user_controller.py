from fastapi import Response, Depends
from app.usecases.user_usecase import UserUseCase
from app.models.schemas.user_schema import UserUpdate



class UserController():
    def __init__(self, user_usecase: UserUseCase = Depends(UserUseCase)):
        self.user_usecase = user_usecase
    
    async def get_users(self):
        return await self.user_usecase.get_users()
    
    async def get_user_by_id(self, user_id: str):
        return await self.user_usecase.get_user_by_id(user_id)
    
    async def update_user_role(self, user_id: str, user_update: UserUpdate):
        return await self.user_usecase.update_user_role(user_id, user_update)
