from fastapi import Depends, HTTPException, Cookie
from typing import List, Optional
from jose import JWTError, jwt
from ..config.settings import settings

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, access_token: Optional[str] = Cookie(None)):
        if not access_token:
            raise HTTPException(
                status_code=401,
                detail="Not authenticated"
            )
        
        try:
            payload = jwt.decode(
                access_token, 
                settings.JWT_SECRET_KEY, 
                algorithms=[settings.JWT_ALGORITHM]
            )
            role = payload.get("role")
            if role not in self.allowed_roles:
                raise HTTPException(
                    status_code=403,
                    detail="Not enough permissions"
                )
            return payload
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )