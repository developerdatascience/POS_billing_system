from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import Customer
from pydantic import BaseModel

router = APIRouter(prefix="/customers", tags=["Customers"])


class CustomerCreate(BaseModel):
    full_name: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None


@router.post("/", response_model=CustomerCreate)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    new_customer = Customer(**payload.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer