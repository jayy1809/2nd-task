from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.models.schemas.user_schema import UserCreate, UserLogin
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status, Depends, Response

class AuthUseCase:
    def __init__(self, auth_service : AuthService = Depends() ): #db: AsyncIOMotorDatabase
        # self.user_repository = UserRepository(db)
        self.auth_service =  auth_service # AuthService(self.user_repository)

    async def register_user(self, user_data: UserCreate):
        result = await self.auth_service.register(user_data)
        return result  
    
    async def login_user(self, user_data: UserLogin, response: Response):
        result = await self.auth_service.login(user_data, response)
        return result
    
    #     try:
    #         # Business logic for registering a user
    #         result = await self.auth_service.register(
    #             name=user_data.name,
    #             email=user_data.email,
    #             password=user_data.password,
    #             role=user_data.role
    #         )
    #         return result
    #     except Exception as e:
    #         # Handle errors appropriately (could be validation or database-related errors)
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail=f"Error during registration: {str(e)}"
    #         )

    # async def login_user(self, user_data: LoginRequest):
    #     try:
    #         # Business logic for logging in a user (like validating credentials and generating a token)
    #         result = await self.auth_service.login(
    #             email=user_data.email,
    #             password=user_data.password
    #         )
    #         return result
    #     except Exception as e:
    #         # Handle errors like invalid credentials
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail=f"Login failed: {str(e)}"
    #         )
