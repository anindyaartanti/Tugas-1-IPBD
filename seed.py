from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from datetime import date, timedelta
import random

def seed_database():
    # Buat tabel jika belum 
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    print("Seeding customers...")
    customers = []
    for i in range(1, 11):
        customer = models.Customer(
            name=f"Customer {i}",
            phone=f"0812{i:04d}{i:04d}",
            address=f"Jl. Contoh No. {i}, Kota Contoh"
        )
        db.add(customer)
        customers.append(customer)
    db.commit()
    
    print("Seeding products...")
    products = []
    product_names = ["Laptop", "Mouse", "Keyboard", "Monitor", "Printer", 
                     "Speaker", "Webcam", "Headset", "USB Cable", "External HDD"]
    for i, name in enumerate(product_names[:10], 1):
        product = models.Product(
            name=name,
            price=random.randint(100000, 5000000),
            stock=random.randint(5, 100)
        )
        db.add(product)
        products.append(product)
    db.commit()
    
    print("Seeding sales orders with items...")
    for order_num in range(1, 11):
        customer = random.choice(customers)
        order_date = date.today() - timedelta(days=random.randint(0, 30))
        
        order_items = []
        num_items = random.randint(1, 3)
        selected_products = random.sample(products, min(num_items, len(products)))
        
        total_amount = 0
        for product in selected_products:
            quantity = random.randint(1, 5)
            price_per_unit = product.price
            total_amount += quantity * price_per_unit
            order_items.append({
                "product_id": product.id,
                "quantity": quantity,
                "price": price_per_unit
            })
        
        db_order = models.SalesOrder(
            customer_id=customer.id,
            order_date=order_date,
            total_amount=total_amount
        )
        db.add(db_order)
        db.flush()
        
        for item in order_items:
            db_item = models.SalesOrderItem(
                order_id=db_order.id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"]
            )
            db.add(db_item)
            product = db.query(models.Product).filter(models.Product.id == item["product_id"]).first()
            product.stock -= item["quantity"]
        
        db.commit()
    
    print("Seeding completed!")
    db.close()

if __name__ == "__main__":
    seed_database()