from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    url: HttpUrl
    target_price: Optional[float] = None
    platform: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    target_price: Optional[float] = None
    is_active: Optional[bool] = None

class Product(ProductBase):
    id: int
    current_price: Optional[float] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class PriceHistoryCreate(BaseModel):
    product_id: int
    price: float

class PriceHistory(PriceHistoryCreate):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str

class User(UserCreate):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
