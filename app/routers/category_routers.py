from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from typing import List

router = APIRouter(prefix="/categories", tags=["Categories"])

# Create new Category
@router.post("/", response_model=CategoryResponse)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(**payload.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
