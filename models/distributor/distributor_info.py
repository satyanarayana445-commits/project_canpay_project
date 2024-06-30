from db_conn.db import db

class DistributorInfo(db.Model):
    __tablename__ = "DISTRIBUTOR_INFO"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    no_of_orders = db.Column(db.Integer, default=0)
    no_of_cans = db.Column(db.Integer, default=0)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'status': self.status,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'is_active': self.is_active,
            'no_of_orders': self.no_of_orders,
            'no_of_cans': self.no_of_cans
        }
