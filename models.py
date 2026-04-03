from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    address = Column(String)

    # Relasi ke SalesOrder (one-to-many)
    orders = relationship("SalesOrder", back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    stock = Column(Integer)

    # Relasi ke SalesOrderItem (one-to-many)
    order_items = relationship("SalesOrderItem", back_populates="product")


class SalesOrder(Base):
    __tablename__ = "sales_orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_date = Column(Date)
    total_amount = Column(Float)

    # Relasi ke Customer (many-to-one)
    customer = relationship("Customer", back_populates="orders")
    
    # Relasi ke SalesOrderItem (one-to-many)
    items = relationship("SalesOrderItem", back_populates="order")


class SalesOrderItem(Base):
    __tablename__ = "sales_order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("sales_orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer)
    price = Column(Float)

    # Relasi ke SalesOrder (many-to-one)
    order = relationship("SalesOrder", back_populates="items")
    
    # Relasi ke Product (many-to-one)
    product = relationship("Product", back_populates="order_items")