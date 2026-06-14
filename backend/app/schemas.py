from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, PositiveInt, constr


class ProductBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    sku: constr(strip_whitespace=True, min_length=1)
    description: Optional[str] = ""
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str]
    sku: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


class CustomerBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr
    phone: Optional[str] = ""


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: PositiveInt


class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]


class OrderItem(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    product_name: Optional[str] = None

    class Config:
        from_attributes = True


class Order(BaseModel):
    id: int
    customer_id: int
    total_amount: float
    created_at: datetime
    items: List[OrderItem]

    class Config:
        from_attributes = True
