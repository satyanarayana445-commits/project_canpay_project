from db_conn.db import db
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import BigInteger

class CustomerAddress(db.Model):
    __tablename__ = "CUSTOMER_ADDRESS"

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    map_address = Column(String, nullable=False)
    flat_number = Column(String, nullable=False)
    floor_number = Column(Integer, nullable=False)
    building = Column(String, nullable=False)
    landmark = Column(String, nullable=True)
    pin_code = Column(String, nullable=False)
    customer_id = Column(BigInteger, nullable=False)
    address_type = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'map_address': self.map_address,
            'flat_number': self.flat_number,
            'floor_number': self.floor_number,
            'building': self.building,
            'landmark': self.landmark,
            'pin_code': self.pin_code,
            'customer_id': self.customer_id,
            'address_type': self.address_type,
            'is_active': self.is_active
        }
