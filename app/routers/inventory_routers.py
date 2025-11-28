from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.models import Inventory
from app.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse
from app.database.session import get_db
from typing import List


router = APIRouter(prefix="/inventory", tags=["Inventory"])

# Add new inventory record
@router.post("/", response_model=InventoryResponse)
def create_inventory(payload: InventoryCreate, db: Session = Depends(get_db)):
    inventory_check = db.query(Inventory).filter(Inventory.product_id == payload.product_id).first()

    if inventory_check:
        raise HTTPException(400, detail="Inventory record for this product already exists")
    
    new_inventory = Inventory(**payload.dict())
    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)
    return new_inventory


@router.get("/", response_model=List[InventoryResponse])
def get_all_inventory(db: Session = Depends(get_db)):
    inventories = db.query(Inventory).all()
    return inventories

@router.put("/{inventory_id}", response_model=InventoryResponse)
async def update_inventory(inventory_id: int, payload: InventoryUpdate, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()

    if not inventory:
        raise HTTPException(404, detail="Inventory records not found with {}".format(inventory_id))
    
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(inventory, key, value)
    
    db.commit()
    db.refresh(inventory)
    return inventory