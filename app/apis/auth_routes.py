from fastapi import APIRouter, Depends, Response, Request
# from ..config.database import get_database
from ..repositories.user_repository import UserRepository
from ..services.auth_service import AuthService
from ..controllers.auth_controller import AuthController
from ..models.schemas.user_schema import UserCreate, UserLogin
from motor.motor_asyncio import AsyncIOMotorDatabase
# from ..config.settings import settings
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.post("/register")
@limiter.limit("5/minute")
async def register(
    user_data: UserCreate,
    request: Request,
    auth_controller : AuthController = Depends(AuthController),
    
):
    result = await auth_controller.register(user_data)
    return {
            "data": result,
            "status_code": 201,
            "detail": "User registered successfully",
            "error": ""
        }

@router.post("/login")
@limiter.limit("5/minute")
async def login(
    user_data: UserLogin,
    request: Request,
    response: Response,
    auth_controller : AuthController = Depends(AuthController),
):
    result = await auth_controller.login(user_data, response)
    return {
            "data": result,
            "status_code": 200,
            "detail": "Login successful",
            "error": ""
        }

# async def register(
#     user_data: UserCreate,
#     db: AsyncIOMotorDatabase = Depends(get_database)
# ):
#     try:
#         user_repository = UserRepository(db)
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

# @router.post("/login")
# @limiter.limit("5/minute")
# async def login(
#     user_data: UserLogin,
#     response: Response,
#     db: AsyncIOMotorDatabase = Depends(get_database)
# ):
#     try:
#         user_repository = UserRepository(db)
#         auth_service = AuthService(user_repository)
#         result = await auth_service.login(
#             email=user_data.email,
#             password=user_data.password
#         )
        
#         # Set cookie
#         response.set_cookie(
#             key="access_token",
#             value=result["access_token"],
#             httponly=True,
#             secure=False,  # Set to True in production with HTTPS
#             max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
#             samesite="lax"
#         )
        
#         return {
#             "data": result,
#             "status_code": 200,
#             "detail": "Login successful",
#             "error": ""
#         }
#     except Exception as e:
#         return {
#             "data": {},
#             "status_code": getattr(e, "status_code", 500),
#             "detail": str(e),
#             "error": str(e)
#         }