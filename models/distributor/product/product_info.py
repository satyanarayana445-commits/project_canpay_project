from db_conn.db import db

class ProductInfo(db.Model):
    __tablename__ = "PRODUCT_INFO"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    description = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'is_active': self.is_active,
            'description': self.description,
            'image': self.image
        }
