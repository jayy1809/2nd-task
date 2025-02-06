from pydantic import BaseModel, EmailStr, validator, field_validator
from typing import Literal

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str  
    role: Literal["admin", "buyer", "seller"] 

    @field_validator('name')
    def validate_name(cls, v):
        if not v or len(v) > 50 or len(v) == 0:
            raise ValueError('Name cannot be empty or longer than 50 characters')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if not v or len(v) > 100 or len(v) == 0:
            raise ValueError('Password cannot be empty or longer than 100 characters')
        return v

    @field_validator('role')
    def validate_role(cls, v):
        valid_roles = ['buyer', 'seller', 'admin']
        if v not in valid_roles:
            raise ValueError(f'Role must be one of: {", ".join(valid_roles)}')
        return v
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class UserUpdate(BaseModel):
    role: Literal["admin", "buyer", "seller"]

    @field_validator('role')
    def validate_role(cls, v):
        valid_roles = ['buyer', 'seller', 'admin']
        if v not in valid_roles:
            raise ValueError(f'Role must be one of: {", ".join(valid_roles)}')
        return v