from fastapi import Response, Depends
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.models.schemas.user_schema import UserCreate, UserLogin
from app.config.database import database, Database, get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.usecases.auth_usecase import AuthUseCase

class AuthController:
    def __init__(self, auth_usecase : AuthUseCase = Depends(AuthUseCase)):
        self.auth_usecase = auth_usecase

    async def register(self, user_data: UserCreate): # db: AsyncIOMotorDatabase = Depends(get_database)
        return await self.auth_usecase.register_user(user_data)
    
    async def login(self, user_data: UserLogin, response: Response):
        return await self.auth_usecase.login_user(user_data, response)
    #     try:
    #         # user_repository = UserRepository(db)
    #         auth_service = AuthService(user_repository)
    #         result = await auth_service.register(
    #             name=user_data.name,
    #             email=user_data.email,
    #             password=user_data.password,
    #             role=user_data.role
    #         )
            
    #         return {
    #             "data": result,
    #             "status_code": 201,
    #             "detail": "User registered successfully",
    #             "error": ""
    #         }
    #     except Exception as e:
    #         return {
    #             "data": {},
    #             "status_code": getattr(e, "status_code", 500),
    #             "detail": str(e),
    #             "error": str(e)
    #         }
    #     # return await register_user(user_data)

    # async def login(self, user_data: LoginRequest):
    #     return await login_user(user_data)