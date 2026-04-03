from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class CustomerBase(BaseModel):
    name: str
    phone: str
    address: str


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    price: float
    stock: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


class SalesOrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float


class SalesOrderItemCreate(SalesOrderItemBase):
    pass


class SalesOrderItem(SalesOrderItemBase):
    id: int

    class Config:
        from_attributes = True


class SalesOrderBase(BaseModel):
    customer_id: int
    order_date: date
    total_amount: float


class SalesOrderCreate(SalesOrderBase):
    items: List[SalesOrderItemCreate]


class SalesOrder(SalesOrderBase):
    id: int
    items: List[SalesOrderItem] = []

    class Config:
        from_attributes = True