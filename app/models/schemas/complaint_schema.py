from typing import Literal, Optional
from pydantic import BaseModel, field_validator


class ComplaintCreate(BaseModel):
    user_id: str
    order_id: str
    product_id: str
    issue: str
    image_url: Optional[str]
    status: Optional[Literal["open", "rejected"]] = "open"

    @field_validator('issue')
    def validate_issue(cls, v):
        if not v or len(v) > 1000 or len(v) == 0:
            raise ValueError('Issue cannot be empty or longer than 1000 characters')
        return v
    
    @field_validator('status')
    def validate_status(cls, v):
        valid_statuses = ['open', 'rejected']
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v
    
    @field_validator('order_id', 'user_id' ,'product_id')
    def validate_ids(cls, v):
        if len(v) != 24:
            raise ValueError('Invalid ID')