from flask import jsonify,request, Blueprint
from sqlalchemy import and_, or_
from db_conn.db import db_connection
from models.customer.customer_address import CustomerAddress
from models.customer.customer_info import CustomerInfo

app = Blueprint('customer_info_blueprint', __name__)
session =  db_connection()


# get customer info by id
@app.route('/info/<int:customer_id>', methods=['GET'])
def get_customer_info_by_id(customer_id):
    customer_data = CustomerInfo.query.filter_by(id=customer_id).first()
    return jsonify(status=200, success=True, data=customer_data), 200

# update customer info (name and email)
@app.route('/info', methods=['PUT'])
def update_customer_info():
    customer_details = request.get_json()
    customer_id = customer_details.get('customerId')
    name = customer_details.get('name')
    email = customer_details.get('email')
    customer_data = CustomerInfo.query.filter_by(id=customer_id).first()
    customer_data.name = name
    customer_data.email = email
    session.commit()
    session.close()
    return jsonify(status=200, success=True, data="customer_data"), 200

# get all active customer addresses
@app.route('/addresses/<int:customer_id>', methods=['GET'])
def get_all_customer_addresses(customer_id):
    addresses_data = CustomerAddress.query.filter_by(customer_id=customer_id, is_active=True).all()
    return jsonify(status=200, success=True, data=addresses_data), 200

# create customer address
@app.route('/address', methods=['POST'])
def create_customer_address():
    address_details = request.get_json()
    latitude = address_details.get('latitude')
    longitude = address_details.get('longitude')
    map_address = address_details.get('mapAddress')
    flat_number = address_details.get('flatNumber')
    floor_number = address_details.get('floorNumber')
    building = address_details.get('building')
    landmark = address_details.get('landmark')
    pin_code = address_details.get('pinCode')
    customer_id = address_details.get('customerId')
    address_type = address_details.get('addressType')
    CustomerAddress(latitude=latitude, longitude=longitude, map_address=map_address, flat_number=flat_number, floor_number=floor_number, building=building, landmark=landmark, pin_code=pin_code, customer_id=customer_id, address_type=address_type)
    session.add(CustomerAddress)
    session.commit()
    session.close()
    return jsonify(status=200, success=True, data="addresses_data"), 200

# update customer address
@app.route('/address/<int:customer_id>', methods=['PUT'])
def update_customer_address(customer_id):
    address_details = request.get_json()
    address_id = address_details.get('addressId')
    latitude = address_details.get('latitude')
    longitude = address_details.get('longitude')
    map_address = address_details.get('mapAddress')
    flat_number = address_details.get('flatNumber')
    floor_number = address_details.get('floorNumber')
    building = address_details.get('building')
    landmark = address_details.get('landmark')
    pin_code = address_details.get('pinCode')
    address_type = address_details.get('addressType')
    address_data = CustomerAddress.query.filter_by(id=address_id).first()
    address_data.latitude = latitude
    address_data.longitude = longitude
    address_data.map_address = map_address
    address_data.flat_number = flat_number
    address_data.floor_number = floor_number
    address_data.building = building
    address_data.landmark = landmark
    address_data.pin_code = pin_code
    address_data.address_type = address_type
    session.commit()
    session.close()
    return jsonify(status=200, success=True, data="addresses_data"), 200

# delete customer address
@app.route('/address/<int:address_id>', methods=['DELETE'])
def delete_customer_address(address_id):
    address_data = CustomerAddress.query.filter_by(id=address_id).first()
    address_data.is_active = False
    session.commit()
    session.close()
    return jsonify(status=200, success=True, data="addresses_data"), 200
