from pydantic import BaseModel, field_validator, Field
from typing import Any, Optional, List


class CartItem(BaseModel):
    product_id: str
    quantity: int

    @field_validator('quantity')
    def validate_quantity(cls, v):
        if v < 1:
            raise ValueError('Quantity must be greater than 0')
        return v
    
    @field_validator('product_id')
    def validate_id(cls, v):
        if len(v) != 24: #becaaase mongodb's object id is a 24-character longggg hexadecimal string
            raise ValueError('ID must be a 24-character hexadecimal string, wrong user_id or product_id')
        return v