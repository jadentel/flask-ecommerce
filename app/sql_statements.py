from app import db
from .models import *
from sqlalchemy import update


def remove_item(product_code, quantity):

    update_statement = (
        update(Product)
        .where(Product.Code == product_code)
        .values(Stock=Product.Stock - quantity)
    )
    db.session.execute(update_statement)
    db.session.commit()
