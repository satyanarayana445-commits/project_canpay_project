from flask import jsonify,request, Blueprint
from sqlalchemy import and_, or_
from db_conn.db import db_connection
from models.customer.customer_address import CustomerAddress
from models.customer.customer_info import CustomerInfo

distributor_customer_info_blueprint = Blueprint('distributor_customer_info_blueprint', __name__)
session =  db_connection()


# get customer info by id
@distributor_customer_info_blueprint.route('/info/<int:customer_id>', methods=['GET'])
def get_customer_info_by_id(customer_id):
    customer_data = CustomerInfo.query.filter_by(id=customer_id).first()
    return jsonify(status=200, success=True, data=customer_data), 200

# update no of cans for customer
@distributor_customer_info_blueprint.route('/cans', methods=['PUT'])
def update_customer_cans():
    customer_cans_details = request.get_json()
    customer_id = customer_cans_details.get('customerId')
    cans = customer_cans_details.get('cans')
    customer_data = CustomerInfo.query.filter_by(id=customer_id).first()
    customer_data.cans_purchased = cans
    session.commit()
    session.close()
    return jsonify(status=200, success=True, data="customer_data"), 200

# update paylater for customer
@distributor_customer_info_blueprint.route('/paylater', methods=['PUT'])
def update_customer_paylater():
    customer_paylater_details = request.get_json()
    customer_id = customer_paylater_details.get('customerId')
    paylater = customer_paylater_details.get('paylater')
    customer_data = CustomerInfo.query.filter_by(id=customer_id).first()
    customer_data.pay_later = paylater
    session.commit()
    session.close()
    return jsonify(status=200, success=True, data="customer_data"), 200
