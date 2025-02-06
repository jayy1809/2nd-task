from ..repositories.user_repository import UserRepository
from ..models.domain.user import User
from ..utils.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, Depends, Response
from app.models.schemas.user_schema import UserCreate, UserLogin
from app.config.settings import settings

class AuthService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    async def register(self, user_data: UserCreate):
        existing_user = await self.user_repository.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        hashed_password = get_password_hash(user_data.password)
        user = User(name=user_data.name, email=user_data.email, password_hash=hashed_password, role=user_data.role)
        user_id = await self.user_repository.create_user(user)
        
        return {
            "user_id": user_id,
            "email": user_data.email,
            "role": user_data.role
        }

    async def login(self, user_data: UserLogin, response: Response):
        user = await self.user_repository.get_user_by_email(user_data.email)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not verify_password(user_data.password, user["password_hash"]):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token(
            data={"sub": str(user["_id"]), "role": user["role"]},
            expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False, samesite="lax")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": user["role"]
        }
