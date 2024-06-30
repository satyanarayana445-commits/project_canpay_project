from flask import jsonify,request, Blueprint
from sqlalchemy import and_, or_
from db_conn.db import db_connection
from models.customer.customer_address import CustomerAddress
from models.customer.customer_info import CustomerInfo
from models.delivery_agent.delivery_agent_info import DeliveryAgentInfo
import bcrypt

delivery_info_blueprint = Blueprint('delivery_info_blueprint', __name__)
session =  db_connection()


# get delivery_agent info by id
@delivery_info_blueprint.route('/info/<int:delivery_agent>', methods=['GET'])
def get_customer_info_by_id(delivery_agent):
    delivery_agent_data = DeliveryAgentInfo.query.filter_by(id=delivery_agent).first()
    return jsonify(status=200, success=True, data=delivery_agent_data), 200

# update delivery_agent info (name and password)
@delivery_info_blueprint.route('/info', methods=['PUT'])
def update_customer_info():
    delivery_agent_details = request.get_json()
    delivery_agent_id = delivery_agent_details.get('deliveryAgentId')
    name = delivery_agent_details.get('name')
    password = delivery_agent_details.get('password')
    delivery_agent_data = DeliveryAgentInfo.query.filter_by(id=delivery_agent_id).first()

    if name:
        delivery_agent_data.name = name
    # encrypt password
    password = encrypt_password(password)
    delivery_agent_data.password = password

    session.commit()
    session.close()
    return jsonify(status=200, success=True, data="delivery_agent_data"), 200

def encrypt_password(password):
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    # Generate a salt and hash the password
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Convert the hashed password back to a string for storage
    return hashed_password.decode('utf-8')