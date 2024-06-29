from db_conn.db import db

class CustomerOrderPayment(db.Model):
    __tablename__ = "CUSTOMER_ORDER_PAYMENT"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.BigInteger, nullable=False)
    gateway_payment_id = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    currency = db.Column(db.String, nullable=False)
    attempts = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'gateway_payment_id': self.gateway_payment_id,
            'amount': self.amount,
            'status': self.status,
            'currency': self.currency,
            'attempts': self.attempts
        }
