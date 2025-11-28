from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class InventorySchema(BaseModel):
    product_id: int
    quantity_available: Optional[int] = 0
    reorder_level: Optional[int] = 0
    last_restock_date: Optional[date] = None


class InventoryCreate(InventorySchema):
    pass

class InventoryUpdate(InventorySchema):
    pass

class InventoryResponse(InventorySchema):
    inventory_id: int

    class Config:
        orm_mode = True