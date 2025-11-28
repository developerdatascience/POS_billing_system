from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database.session import get_db
from app.database.models import Sale, SalesItem
from app.schemas.sales import SalesCreate
from app.utils.inventory import reduce_inventory
from app.utils.add_payment_status import add_payment_status

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post("/")
def create_sales(payload: SalesCreate, db: Session = Depends(get_db)):

    try:
        # 1️⃣ CREATE SALE OBJECT (NO COMMIT)
        sale = Sale(
            customer_id = payload.customer_id,
            total_quantity = sum(item.quantity for item in payload.items),
            total_amount = sum(item.quantity * item.selling_price for item in payload.items),
            discount_amount = (payload.discount_pct or 0) / 100
                            * sum(item.quantity * item.selling_price for item in payload.items),
            final_amount = 0,
            payment_mode = payload.payment_mode
        )
        db.add(sale)
        db.flush()   # get sale.sale_id without commit

        total_price = 0

        # 2️⃣ LOOP THROUGH SALE ITEMS
        for item in payload.items:
            discounted_price = item.selling_price * (1 - (payload.discount_pct or 0) / 100)
            item_total = item.quantity * discounted_price
            total_price += item_total

            sale_item = SalesItem(
                sale_id = sale.sale_id,
                product_id = item.product_id,
                quantity = item.quantity,
                selling_price = item.selling_price,
                discount_pct = payload.discount_pct or 0,
                total_price = item_total
            )
            db.add(sale_item)

            # Update inventory — keep inside same transaction
            reduce_inventory(db, item.product_id, item.quantity)

        # 3️⃣ UPDATE FINAL AMOUNTS
        sale.total_price = total_price
        sale.final_amount = total_price

        # 4️⃣ RECORD PAYMENT
        payment = add_payment_status(
            db,
            sale_id = sale.sale_id,
            amount_paid = sale.total_price,
            payment_mode = payload.payment_mode,
            payment_status = "SUCCESS"
        )

        # 5️⃣ ONE COMMIT FOR EVERYTHING
        db.commit()

        # Refresh objects only after commit
        db.refresh(sale)
        db.refresh(payment)

        return {
            "message": "Sale created successfully",
            "sale_id": sale.sale_id,
            "payment_id": payment.transaction_id
        }

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(400, f"Database error: {str(e)}")

    except Exception as e:
        db.rollback()
        raise HTTPException(400, str(e))
