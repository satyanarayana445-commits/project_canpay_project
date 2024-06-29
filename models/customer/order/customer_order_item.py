from db_conn.db import db

class CustomerOrderItem(db.Model):
    __tablename__ = "CUSTOMER_ORDER_ITEM"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.BigInteger, nullable=False)
    product_id = db.Column(db.BigInteger, nullable=False)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price
        }
