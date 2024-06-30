from flask import jsonify,request, Blueprint
from db_conn.db import db_connection
from models.delivery_agent.delivery_agent_info import DeliveryAgentInfo
import bcrypt
from models.distributor.distributor_info import DistributorInfo

distributor_delivery_agent_info_blueprint = Blueprint('distributor_delivery_agent_info_blueprint', __name__)
session =  db_connection()


# add new delivery agent to distributor
@distributor_delivery_agent_info_blueprint.route('/add_delivery_agent', methods=['POST'])
def add_delivery_agent():
    delivery_agent_details = request.get_json()
    name = delivery_agent_details.get('name')
    password = delivery_agent_details.get('password')
    phone_number = delivery_agent_details.get('phoneNumber')
    distributor_id = delivery_agent_details.get('distributorId')
    DeliveryAgentInfo(name=name, password=password, phone_number=phone_number, distributor_id=distributor_id)
    session.add(DeliveryAgentInfo)
    session.commit()
    session.close()
    response = {
        'name': name,
        'phoneNumber': phone_number,
        'distributorId': distributor_id
    }
    return jsonify(status=200, success=True, data=response), 200

# get all delivery agents for the distributor
@distributor_delivery_agent_info_blueprint.route('/delivery_agents/<int:distributor_id>', methods=['GET'])
def get_all_delivery_agents(distributor_id):
    delivery_agents_data = DeliveryAgentInfo.query.filter_by(distributor_id=distributor_id).all()
    return jsonify(status=200, success=True, data=delivery_agents_data), 200

# get delivery agent info by id
@distributor_delivery_agent_info_blueprint.route('/delivery_agent/<int:delivery_agent_id>', methods=['GET'])
def get_delivery_agent_info_by_id(delivery_agent_id):
    delivery_agent_data = DeliveryAgentInfo.query.filter_by(id=delivery_agent_id).first()
    return jsonify(status=200, success=True, data=delivery_agent_data), 200

def encrypt_password(password):
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    # Generate a salt and hash the password
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Convert the hashed password back to a string for storage
    return hashed_password.decode('utf-8')
