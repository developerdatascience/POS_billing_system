from app.database.models import Inventory

def reduce_inventory(db, product_id: int, quantity: int):
    product = db.query(Inventory).filter(Inventory.product_id == product_id).first()

    if not product:
        raise Exception("Inventory record not found")
    
    if product.quantity_available < quantity:
        raise Exception("Not Enough stock")
    
    product.quantity_available -= quantity
    db.commit()


def increase_inventory(db, product_id: int, quantity: int):
    product = db.query(Inventory).filter(Inventory.product_id == product_id).first()

    if not product:
        raise Exception("Inventory record not found")
    
    if product.quantity_available < quantity:
        raise Exception("Not Enough stock")
    
    product.quantity_available += quantity
    db.commit()
    
    

