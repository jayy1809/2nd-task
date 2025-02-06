from pydantic import BaseModel, field_validator, Field
from typing import Any, Optional, List



class ProductCreate(BaseModel):
    title: str
    description: str
    category: str
    price: float
    rating: float
    brand: str
    images: List[str]
    seller_id : str
    thumbnail: Optional[str] = None
    
    @field_validator('title', 'category', 'brand')
    def validate_length(cls, v):
        if len(v) > 200:
            raise ValueError('Fields must be less than 200 characters')
        return v
    
    @field_validator('description')
    def validate_description(cls, v):
        if len(v) > 2000:
            raise ValueError('Description must be less than 2000 characters')
        return v

    @field_validator('title', 'description', 'category')
    def not_empty(cls, v):
        if not v or len(v) == 0:
            raise ValueError('Fields cannot be empty')
        return v

    @field_validator('price', 'rating')
    def validate_price_rating(cls, v):
        if v < 0:
            raise ValueError('Price and rating must be greater than 0')
        return v
    


class ProductUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    category: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    brand: Optional[str] = None
    images: Optional[List[str]] = None
    thumbnail: Optional[str] = None

    @field_validator('title', 'category', 'brand', 'description')
    def empty_string(cls, v):
        if v == "" or len(v) == 0:
            raise ValueError('Fields cannot be empty')
        return v
    
    @field_validator('price')
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price must be greater than 0')
        return v
    
    @field_validator('price')
    def price_length(cls, v):
        if len(str(v)) > 10:
            raise ValueError('Price must be less than 10 digits')
        return v
