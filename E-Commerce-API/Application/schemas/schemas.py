from pydantic import BaseModel
from typing import Optional
from enum import Enum
from pydantic import EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_id: int
    status: OrderStatus = OrderStatus.PENDING

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: OrderStatus

class OrderResponse(OrderBase):
    id: int
    class Config:
        from_attributes = True
