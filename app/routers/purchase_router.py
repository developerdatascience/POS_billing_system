from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database.models import PurchaseOrder, PurchaseItem
from app.utils.inventory import increase_inventory
from app.database.session import get_db
from pydantic import BaseModel
from typing import List


router = APIRouter(prefix="/purchases", tags=["Purchases"])

class PurchaseItemSchema(BaseModel):
    pass