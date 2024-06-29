from db_conn.db import db

class DeliveryAgentInfo(db.Model):
    __tablename__ = "DELIVERY_AGENT_INFO"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=True)
    distributor_id = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'status': self.status,
            'distributor_id': self.distributor_id,
            'is_active': self.is_active
        }
