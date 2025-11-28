from pydantic import BaseModel
from typing import Optional, List

class SalesItemSchema(BaseModel):
    product_id: int
    quantity: int
    selling_price: float

class SalesCreate(BaseModel):
    # invoice_number: str
    customer_id: int | None = None
    payment_mode: Optional[str] = None
    discount_pct: Optional[float] = 5.0
    items: List[SalesItemSchema]
