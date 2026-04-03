from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import engine, SessionLocal
import models
import schema
import crud

# Buat tabel
def init_db():
    models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Company API", version="1.0")

@app.on_event("startup")
def on_startup():
    init_db()

# Dependency session database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ROOT
@app.get("/")
def root():
    return {"message": "Company API running"}

# CUSTOMER
@app.post("/customers", response_model=schema.Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: schema.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)

@app.get("/customers", response_model=List[schema.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_customers(db, skip=skip, limit=limit)

@app.get("/customers/{customer_id}", response_model=schema.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.put("/customers/{customer_id}", response_model=schema.Customer)
def update_customer(customer_id: int, customer: schema.CustomerCreate, db: Session = Depends(get_db)):
    return crud.update_customer(db, customer_id, customer)

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return crud.delete_customer(db, customer_id)

# PRODUCT
@app.post("/products", response_model=schema.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: schema.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.get("/products", response_model=List[schema.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=schema.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.put("/products/{product_id}", response_model=schema.Product)
def update_product(product_id: int, product: schema.ProductCreate, db: Session = Depends(get_db)):
    return crud.update_product(db, product_id, product)

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return crud.delete_product(db, product_id)

# SALES ORDER
@app.post("/orders", response_model=schema.SalesOrder, status_code=status.HTTP_201_CREATED)
def create_order(order: schema.SalesOrderCreate, db: Session = Depends(get_db)):
    return crud.create_sales_order(db, order)

@app.get("/orders", response_model=List[schema.SalesOrder])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_sales_orders(db, skip=skip, limit=limit)

@app.get("/orders/{order_id}", response_model=schema.SalesOrder)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_sales_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.put("/orders/{order_id}", response_model=schema.SalesOrder)
def update_order(order_id: int, order: schema.SalesOrderBase, db: Session = Depends(get_db)):
    return crud.update_sales_order(db, order_id, order)

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return crud.delete_sales_order(db, order_id)