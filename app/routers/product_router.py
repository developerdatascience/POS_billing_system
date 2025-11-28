from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

# Create new product
@router.post("/", response_model=ProductResponse)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    check = db.query(Product).filter(Product.sku == payload.sku).first()

    if check:
        raise HTTPException(400, detail="SKU alredy exists")
    
    new_product = Product(**payload.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# Get all products
@router.get("/", response_model= List[ProductResponse])
def get_products(db: Session = Depends(get_db), skip: int =0, limit: int = 50):
    return db.query(Product).offset(skip).limit(limit).all()

# Get product by ID
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()

    if not product:
        raise HTTPException(404, detail="Product not found")
    
    return product

# Update product by ID
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()

    if not product:
        raise HTTPException(404, detail="Product not found")
    
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)

    return product

# Delete product by ID
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()

    if not product:
        raise HTTPException(404, detail="Product not found")
    
    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}

