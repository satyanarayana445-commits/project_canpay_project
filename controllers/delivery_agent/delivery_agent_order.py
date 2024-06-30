from datetime import datetime
from flask import jsonify,request, Blueprint
from sqlalchemy import and_, or_, func
from db_conn.db import db_connection
from models.customer.customer_address import CustomerAddress
from models.customer.customer_info import CustomerInfo
from models.customer.order.customer_order import CustomerOrder
from models.customer.order.customer_order_item import CustomerOrderItem
from models.customer.order.customer_order_payment import CustomerOrderPayment
from models.delivery_agent.delivery_agent_info import DeliveryAgentInfo
from models.distributor.distributor_info import DistributorInfo
from models.distributor.product.product_info import ProductInfo

delivery_agent_order_blueprint = Blueprint('delivery_agent_order_blueprint', __name__)
session =  db_connection()

# TODO: Categorise the functionality into different functions and services and modularize the code, also add validation for the request body, add error handling and logging for each API
# Test the APIs using Postman and Swagger, also add unit tests for each API, also add API documentation, have 2 weeks of time to complete whole project

# get all orders for the distributor
@delivery_agent_order_blueprint.route('/orders/<int:distributor_id>', methods=['GET'])
def order_details(distributor_id):
    allowed_statuses = ['ORDER_PLACED', 'PAID', 'CASH_ON_DELIVERY', 'PAY_LATER', 'OUT_FOR_DELIVERY', 'DELIVERED']
    date = datetime.now().date()
    orders_data = CustomerOrder.query.filter(and_(CustomerOrder.distributor_id == distributor_id, CustomerOrder.status.in_(allowed_statuses), CustomerOrder.selected_date == date)).all()
    return jsonify(status=200, success=True, data=orders_data), 200

# get active orders for the distributor
@delivery_agent_order_blueprint.route('/orders/active/<int:distributor_id>', methods=['GET'])
def get_active_orders(distributor_id):
    allowed_statuses = ['ORDER_PLACED', 'PAID', 'CASH_ON_DELIVERY', 'PAY_LATER', 'OUT_FOR_DELIVERY']
    date = datetime.now().date()
    orders_data = CustomerOrder.query.filter(and_(CustomerOrder.distributor_id == distributor_id, CustomerOrder.status.in_(allowed_statuses), CustomerOrder.selected_date == date)).all()

    # order by time slot
    orders_data = sorted(orders_data, key=lambda x: x.selected_slot)
    return jsonify(status=200, success=True, data=orders_data), 200

# get order details by order id
@delivery_agent_order_blueprint.route('/order/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    order_data = CustomerOrder.query.filter_by(id=order_id).first()
    customer_order_items = CustomerOrderItem.query.filter_by(order_id=order_id).all()
    order_items = []
    for item in customer_order_items:
        product = ProductInfo.query.filter_by(id=item.product_id).first()
        order_items.delivery_agent_order_blueprintend({
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

# update order status
@delivery_agent_order_blueprint.route('/order/status', methods=['PUT'])
def update_order_status():
    order_details = request.get_json()
    order_id = order_details.get('orderId')
    delivery_agent_id = order_details.get('deliveryAgentId')
    distributor_data = DeliveryAgentInfo.query.filter_by(delivery_agent_id=delivery_agent_id).first()
    status = order_details.get('status')
    order_data = CustomerOrder.query.filter_by(id=order_id).first()
    order_data.status = status

    if status == 'DELIVERED':
        # get no of cans from order items and update the cans count for the distributor
        order_items = CustomerOrderItem.query.filter_by(order_id=order_id).all()
        cans_count = 0
        for item in order_items:
            if item.product_id == 1:
                cans_count += item.quantity
        
        distributor_data.cans_count -= cans_count
        distributor_data.no_of_orders += 1

    session.commit()
    session.close()

    response = {
        'orderId': order_id,
        'status': status
    }
    return jsonify(status=200, success=True, data=response), 200

# update order payment status for cash on delivery
@delivery_agent_order_blueprint.route('/order/payment/status', methods=['PUT'])
def update_order_payment_status():
    order_details = request.get_json()
    order_id = order_details.get('orderId')
    payment_status = order_details.get('paymentStatus')
    order_data = CustomerOrder.query.filter_by(id=order_id).first()
    order_payment_data = CustomerOrderPayment.query.filter_by(order_id=order_id).first()

    if order_payment_data.status == 'CASE_ON_DELIVERY' and payment_status == 'PAID':
        order_data.status = 'PAID'
        order_payment_data.payment_status = payment_status

    session.commit()
    session.close()

    response = {
        'orderId': order_id,
        'paymentStatus': payment_status
    }
    return jsonify(status=200, success=True, data=response), 200