from datetime import datetime
from flask import jsonify,request, Blueprint
from sqlalchemy import and_, or_, func
from db_conn.db import db_connection
from models.customer.customer_address import CustomerAddress
from models.customer.customer_info import CustomerInfo
from models.customer.order.customer_order import CustomerOrder
from models.customer.order.customer_order_item import CustomerOrderItem
from models.distributor.product.product_info import ProductInfo

distributor_customer_order_blueprint = Blueprint('distributor_customer_order_blueprint', __name__)
session =  db_connection()

# TODO: Categorise the functionality into different functions and services and modularize the code, also add validation for the request body, add error handling and logging for each API
# Test the APIs using Postman and Swagger, also add unit tests for each API, also add API documentation, have 2 weeks of time to complete whole project

# get all orders for the distributor
@distributor_customer_order_blueprint.route('/orders/<int:distributor_id>', methods=['GET'])
def order_details(distributor_id):
    allowed_statuses = ['ORDER_PLACED', 'PAID', 'CASH_ON_DELIVERY', 'PAY_LATER', 'OUT_FOR_DELIVERY', 'DELIVERED']
    date = datetime.now().date()
    orders_data = CustomerOrder.query.filter(and_(CustomerOrder.distributor_id == distributor_id, CustomerOrder.status.in_(allowed_statuses), CustomerOrder.selected_date == date)).all()
    return jsonify(status=200, success=True, data=orders_data), 200

# get active orders for the distributor
@distributor_customer_order_blueprint.route('/orders/active/<int:distributor_id>', methods=['GET'])
def get_active_orders(distributor_id):
    allowed_statuses = ['ORDER_PLACED', 'PAID', 'CASH_ON_DELIVERY', 'PAY_LATER', 'OUT_FOR_DELIVERY']
    date = datetime.now().date()
    orders_data = CustomerOrder.query.filter(and_(CustomerOrder.distributor_id == distributor_id, CustomerOrder.status.in_(allowed_statuses), CustomerOrder.selected_date == date)).all()

    # order by time slot
    orders_data = sorted(orders_data, key=lambda x: x.selected_slot)
    return jsonify(status=200, success=True, data=orders_data), 200

# get order details by order id
@distributor_customer_order_blueprint.route('/order/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    order_data = CustomerOrder.query.filter_by(id=order_id).first()
    customer_order_items = CustomerOrderItem.query.filter_by(order_id=order_id).all()
    order_items = []
    for item in customer_order_items:
        product = ProductInfo.query.filter_by(id=item.product_id).first()
        order_items.distributor_customer_order_blueprintend({
            'product': product.serialize,
            'quantity': item.quantity
        })
    
    customer_details = CustomerInfo.query.filter_by(id=order_data.customer_id).first()
    customer_address = CustomerAddress.query.filter_by(id=order_data.address_id).first()

    response = {
        'order': order_data.serialize,
        'orderItems': order_items,
        'customer': customer_details.serialize,
        'address': customer_address.serialize
    }
    return jsonify(status=200, success=True, data=response), 200
