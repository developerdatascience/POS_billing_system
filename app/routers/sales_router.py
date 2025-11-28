from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.models import Sale, SalesItem
from app.database.session import get_db
from app.utils.inventory import reduce_inventory
from app.utils.add_payment_status import add_payment_status
from app.schemas.sales import SalesCreate, SalesItemSchema
from app.database.models import PaymentTransaction

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post("/")
def create_sales(payload: SalesCreate, db: Session = Depends(get_db)):
    sale = Sale(
        # invoice_number = payload.invoice_number,
        customer_id = payload.customer_id,
        total_quantity = sum(item.quantity for item in payload.items),
        total_amount = sum(item.quantity * item.selling_price for item in payload.items),
        discount_amount = (payload.discount_pct / 100) * sum(item.quantity * item.selling_price for item in payload.items) if payload.discount_pct else 0,
        final_amount = 0,  # will be updated after adding items
        payment_mode = payload.payment_mode
        )
    db.add(sale)
    db.commit()
    db.refresh(sale)

    quantity = 0
    total_price = 0
    for item in payload.items:
        item_total = item.quantity * (item.selling_price * (1 - (payload.discount_pct / 100) if payload.discount_pct else 1))
        total_price += item_total

        sale_item = SalesItem(
            sale_id = sale.sale_id,
            product_id = item.product_id,
            quantity = item.quantity,
            selling_price = item.selling_price,
            discount_pct = payload.discount_pct if payload.discount_pct else 0,
            total_price = item_total
        )
        
        db.add(sale_item)

        # update inventory
        try:
            reduce_inventory(db, item.product_id, item.quantity)
        except Exception as e:
            raise HTTPException(400, detail=str(e))
    
    # update the sale record with the computed totals and commit once
    try:
        sale.total_price = total_price # type: ignore
        sale.final_amount = sum(item.total_price for item in sale.items) # type: ignore
        db.add(sale)
        db.commit()
    except Exception:
        db.rollback()
        raise

    if sale:
        add_payment_status(
            db,
            sale_id=sale.sale_id, # type: ignore
            amount_paid=sale.total_price,  # type: ignore
            payment_mode=payload.payment_mode, # type: ignore
            payment_status="SUCCESS"  # assuming payment is successful for this example
        )
    else:
        add_payment_status(
            db,
            sale_id=sale.sale_id,
            amount_paid=0,
            payment_mode=payload.payment_mode, # type: ignore
            payment_status="FAILED"
        )

    return {"message": "Sale created successfully", "sale_id": sale.sale_id}


