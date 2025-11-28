# database/models.py

from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey,
    Date, DateTime, Numeric, Boolean, JSON, event, text
)
from sqlalchemy.orm import relationship
from datetime import datetime

from sqlalchemy.sql import func
from .base import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), nullable=False)  # admin / staff
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    purchases = relationship("PurchaseOrder", back_populates="creator")
    sales = relationship("Sale", back_populates="creator")
    logs = relationship("AuditLog", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    product_name = Column(String(150), nullable=False)
    sku = Column(String(50), unique=True, nullable=False)
    barcode = Column(String(50))
    unit = Column(String(20))
    description = Column(Text)
    min_stock_level = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    purchase_items = relationship("PurchaseItem", back_populates="product")
    sales_items = relationship("SalesItem", back_populates="product")
    return_items = relationship("SalesReturnItem", back_populates="product")


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True)
    supplier_name = Column(String(150), nullable=False)
    contact_name = Column(String(150))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    gst_number = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    purchases = relationship("PurchaseOrder", back_populates="supplier")


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    purchase_id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"))
    invoice_number = Column(String(100))
    purchase_date = Column(Date, nullable=False)
    total_amount = Column(Numeric(10,2), default=0)
    tax_amount = Column(Numeric(10,2), default=0)
    discount_amount = Column(Numeric(10,2), default=0)
    final_amount = Column(Numeric(10,2), default=0)
    created_by = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    supplier = relationship("Supplier", back_populates="purchases")
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete")
    creator = relationship("User", back_populates="purchases")


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    purchase_item_id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey("purchase_orders.purchase_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer, nullable=False)
    cost_price = Column(Numeric(10,2), nullable=False)
    selling_price = Column(Numeric(10,2), nullable=False)
    tax_percent = Column(Numeric(5,2))
    total_price = Column(Numeric(10,2), nullable=False)

    purchase = relationship("PurchaseOrder", back_populates="items")
    product = relationship("Product", back_populates="purchase_items")


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), unique=True)
    quantity_available = Column(Integer, default=0)
    last_restock_date = Column(Date)
    last_updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now)

    product = relationship("Product", back_populates="inventory")


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    full_name = Column(String(150))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    sales = relationship("Sale", back_populates="customer")

class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True)
    invoice_number = Column(String(100), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    sale_date = Column(DateTime, default=datetime.now())
    total_quantity = Column(Integer, default=0)
    total_amount = Column(Numeric(10,2), default=0)
    discount_amount = Column(Numeric(10,2), default=0)
    tax_amount = Column(Numeric(10,2), default=0)
    final_amount = Column(Numeric(10,2), default=0)
    payment_mode = Column(String(20))  # cash, card, upi, etc.
    created_by = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default=datetime.now())

    customer = relationship("Customer", back_populates="sales")
    creator = relationship("User", back_populates="sales")
    items = relationship("SalesItem", back_populates="sale", cascade="all, delete")
    returns = relationship("SalesReturn", back_populates="sale")

@event.listens_for(Sale, "before_insert")
def generate_invoice(mapper, connection, target):
    today = datetime.now().strftime("%Y%m%d")
    pattern = f"INV-{today}-%"

    stmt = text("""
        SELECT invoice_number
        FROM sales
        WHERE invoice_number LIKE :pattern
        ORDER BY invoice_number DESC
        LIMIT 1
    """)

    result = connection.execute(stmt, {"pattern": pattern}).fetchone()

    if result:
        last_number = int(result[0].split("-")[-1])
        new_number = last_number + 1
    else:
        new_number = 1

    target.invoice_number = f"INV-{today}-{new_number:06d}"




class SalesItem(Base):
    __tablename__ = "sales_items"

    sales_item_id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer, nullable=False)
    selling_price = Column(Numeric(10,2), nullable=False)
    tax_percent = Column(Numeric(5,2))
    discount_pct = Column(Numeric(10, 2))
    total_price = Column(Numeric(10,2), nullable=False)

    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", back_populates="sales_items")


class SalesReturn(Base):
    __tablename__ = "sales_returns"

    return_id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"))
    return_date = Column(Date, nullable=False)
    reason = Column(Text)
    refunded_amount = Column(Numeric(10,2), default=0)

    sale = relationship("Sale", back_populates="returns")
    items = relationship("SalesReturnItem", back_populates="return_record", cascade="all, delete")


class SalesReturnItem(Base):
    __tablename__ = "sales_return_items"

    return_item_id = Column(Integer, primary_key=True)
    return_id = Column(Integer, ForeignKey("sales_returns.return_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer, nullable=False)
    refund_amount = Column(Numeric(10,2), nullable=False)

    return_record = relationship("SalesReturn", back_populates="items")
    product = relationship("Product", back_populates="return_items")

class TaxRate(Base):
    __tablename__ = "tax_rates"

    tax_id = Column(Integer, primary_key=True)
    tax_name = Column(String(50))
    tax_percent = Column(Numeric(5,2))


class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"

    transaction_id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"))
    amount_paid = Column(Numeric(10,2))
    payment_mode = Column(String(20))
    payment_status = Column(String(20))  # 'SUCCESS', 'FAILED', 'PENDING'
    reference_number = Column(String(100))
    payment_date = Column(DateTime, default=datetime.now())

    sale = relationship("Sale")

# Create a function to generate 10 digit reference_number before inserting a PaymentTransaction
@event.listens_for(PaymentTransaction, "before_insert")
def generate_reference_number(mapper, connection, target):
    import random
    import string

    reference_number = ''.join(random.choices(string.digits, k=10))
    target.reference_number = reference_number

class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    action = Column(Text)
    table_name = Column(String(50))
    record_id = Column(Integer)
    old_data = Column(JSON)
    new_data = Column(JSON)
    action_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="logs")
