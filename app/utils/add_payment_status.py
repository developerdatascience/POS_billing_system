from app.database.models import PaymentTransaction

def add_payment_status(db, sale_id: int, amount_paid: float, payment_mode: str, payment_status: str):
    payment = PaymentTransaction(
        sale_id=sale_id,
        amount_paid=amount_paid,
        payment_mode=payment_mode,
        payment_status=payment_status
    )
    db.add(payment)
    # db.commit()
    # db.refresh(payment)
    # return {"message": "Payment transaction recorded", "transaction_id": payment.transaction_id}
    return payment