from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import date
from typing import List, Optional

import models
import schema

# CUSTOMER
def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schema.CustomerCreate):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer_update: schema.CustomerCreate):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in customer_update.dict().items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return {"ok": True}

# PRODUCT
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schema.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: schema.ProductCreate):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product_update.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"ok": True}

# SALES ORDER (with items)
def get_sales_order(db: Session, order_id: int):
    return db.query(models.SalesOrder)\
             .options(selectinload(models.SalesOrder.items))\
             .filter(models.SalesOrder.id == order_id).first()

def get_sales_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SalesOrder)\
             .options(selectinload(models.SalesOrder.items))\
             .offset(skip).limit(limit).all()

def create_sales_order(db: Session, order: schema.SalesOrderCreate):
    customer = get_customer(db, order.customer_id)
    if not customer:
        raise HTTPException(status_code=400, detail="Customer not found")
    
    total_amount = 0.0
    for item in order.items:
        product = get_product(db, item.product_id)
        if not product:
            raise HTTPException(status_code=400, detail=f"Product id {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        total_amount += item.quantity * item.price
    
    db_order = models.SalesOrder(
        customer_id=order.customer_id,
        order_date=order.order_date,
        total_amount=total_amount
    )
    db.add(db_order)
    db.flush()
    
    for item in order.items:
        db_item = models.SalesOrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)
        product = get_product(db, item.product_id)
        product.stock -= item.quantity
        db.add(product)
    
    db.commit()
    db.refresh(db_order)
    db_order.items = [item for item in db_order.items]
    return db_order

def update_sales_order(db: Session, order_id: int, order_update: schema.SalesOrderBase):
    db_order = get_sales_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Sales Order not found")
    update_data = order_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_sales_order(db: Session, order_id: int):
    db_order = get_sales_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Sales Order not found")
    
    for item in db_order.items:
        product = get_product(db, item.product_id)
        if product:
            product.stock += item.quantity
            db.add(product)
    
    db.delete(db_order)
    db.commit()
    return {"ok": True}