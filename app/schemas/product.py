from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    product_name: str
    sku: str
    barcode: Optional[str] = None
    unit: Optional[str] = None
    min_stock_level: Optional[int] = None
    category_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    product_id: int

    class Config:
        orm_mode = True
