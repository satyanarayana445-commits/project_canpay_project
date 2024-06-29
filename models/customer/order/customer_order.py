from db_conn.db import db

class CustomerOrder(db.Model):
    __tablename__ = "CUSTOMER_ORDER"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.BigInteger, nullable=False)
    address_id = db.Column(db.BigInteger, nullable=False)
    distributor_id = db.Column(db.BigInteger, nullable=False)
    selected_date = db.Column(db.DateTime, nullable=False)
    selected_slot = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    special_instruction = db.Column(db.String, nullable=True)
    delivery_charges = db.Column(db.Integer, nullable=False)
    item_total = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    delivery_agent_id = db.Column(db.BigInteger, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    is_paid = db.Column(db.Boolean, nullable=False)
    pay_later = db.Column(db.Boolean, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'address_id': self.address_id,
            'distributor_id': self.distributor_id,
            'selected_date': self.selected_date,
            'selected_slot': self.selected_slot,
            'status': self.status,
            'special_instruction': self.special_instruction,
            'delivery_charges': self.delivery_charges,
            'item_total': self.item_total,
            'total': self.total,
            'delivery_agent_id': self.delivery_agent_id,
            'delivered_at': self.delivered_at,
            'is_paid': self.is_paid,
            'pay_later': self.pay_later
        }
