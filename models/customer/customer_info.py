from db_conn.db import db
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import BigInteger

class CustomerInfo(db.Model):
    __tablename__ = "CUSTOMER_INFO"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    primary_address_id = Column(BigInteger, nullable=True)
    cans_purchased = Column(Integer, default=0)
    pay_later = Column(Boolean, default=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)


    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'avatar': self.avatar,
            'primary_address_id': self.primary_address_id,
            'cans_purchased': self.cans_purchased,
            'pay_later': self.pay_later,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
