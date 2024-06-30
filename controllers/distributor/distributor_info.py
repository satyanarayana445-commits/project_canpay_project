from flask import jsonify,request, Blueprint
from db_conn.db import db_connection
from models.delivery_agent.delivery_agent_info import DeliveryAgentInfo
import bcrypt
from models.distributor.distributor_info import DistributorInfo

distributor_info_blueprint = Blueprint('distributor_info_blueprint', __name__)
session =  db_connection()


# get all distributors
@distributor_info_blueprint.route('/distributors', methods=['GET'])
def get_all_distributors():
    distributors_data = DistributorInfo.query.all()
    return jsonify(status=200, success=True, data=distributors_data), 200

# get distributor info by id
@distributor_info_blueprint.route('/info/<int:distributor_id>', methods=['GET'])
def get_distributor_info_by_id(distributor_id):
    distributor_data = DistributorInfo.query.filter_by(id=distributor_id).first()
    return jsonify(status=200, success=True, data=distributor_data), 200

# update distributor info (name and password)
@distributor_info_blueprint.route('/info', methods=['PUT'])
def update_distributor_info():
    distributor_details = request.get_json()
    distributor_id = distributor_details.get('distributorId')
    name = distributor_details.get('name')
    password = distributor_details.get('password')
    distributor_data = DistributorInfo.query.filter_by(id=distributor_id).first()

    if name:
        distributor_data.name = name
    # encrypt password
    password = encrypt_password(password)
    distributor_data.password = password

    session.commit()
    session.close()
    return jsonify(status=200, success=True, data="Updated successfuly"), 200

# add new distributor (temporarily, will be removed in future)
@distributor_info_blueprint.route('/add_distributor', methods=['POST'])
def add_distributor():
    distributor_details = request.get_json()
    name = distributor_details.get('name')
    password = distributor_details.get('password')
    phone_number = distributor_details.get('phoneNumber')
    latitude = distributor_details.get('latitude')
    longitude = distributor_details.get('longitude')
    DistributorInfo(name=name, password=password, phone_number=phone_number, latitude=latitude, longitude=longitude)
    session.add(DistributorInfo)
    session.commit()
    session.close()
    response = {
        'name': name,
        'phoneNumber': phone_number
    }
    return jsonify(status=200, success=True, data=response), 200

# update cans count for distributor
@distributor_info_blueprint.route('/cans', methods=['PUT'])
def update_distributor_cans():
    distributor_cans_details = request.get_json()
    distributor_id = distributor_cans_details.get('distributorId')
    cans_count = distributor_cans_details.get('cansCount')
    distributor_data = DistributorInfo.query.filter_by(id=distributor_id).first()
    distributor_data.no_of_cans = cans_count
    session.commit()
    session.close()
    return jsonify(status=200, success=True, data="Updated successfuly"), 200

def encrypt_password(password):
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    # Generate a salt and hash the password
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Convert the hashed password back to a string for storage
    return hashed_password.decode('utf-8')
