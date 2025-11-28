from fastapi import FastAPI
from app.routers import (
    product_router, 
    sales_router, 
    customer_router,
    category_routers)

app = FastAPI(title="Inventory Management System")

app.include_router(product_router.router)
app.include_router(sales_router.router)
app.include_router(customer_router.router)
app.include_router(category_routers.router)