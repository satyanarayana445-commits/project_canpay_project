from db_conn.db import db

class Orders(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    order_name = db.Column(db.String(100))


    @property
    def serialize(self):
        return {
        'id': self.id,
        'order_name': self.order_name
        }