from sqlalchemy.orm import Session
from sqlalchemy import and_
from database.models import Product, Sale, PurchaseOrder, Inventory
from app.schemas.schemas import ProductCreate, ProductUpdate
from datetime import date



def create_product(db: Session, product: ProductCreate):
    # Validate expiry_date not in the past
    if product.expiry_date and product.expiry_date < date.today():
        raise ValueError("Expiry date cannot be in the past")
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int =0, limit: int = 100):
    products = db.query(Product).offset(skip).limit(limit).all()
    for p in products:
        p.is_expired = p.expiry_date < date.today() if p.expiry_date else p
    return products


def get_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).all()
    if product:
        product.is_expired = product.expiry_date < date.today() if product.expiry_date else False
    return product

