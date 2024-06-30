from flask import jsonify,request, Blueprint
from sqlalchemy import and_, or_, func
from db_conn.db import db_connection
from geoalchemy2.functions import ST_Point
from models.customer.customer_address import CustomerAddress
from models.customer.order.customer_order import CustomerOrder
from models.customer.order.customer_order_item import CustomerOrderItem
from models.customer.order.customer_order_payment import CustomerOrderPayment
from models.distributor.distributor_info import DistributorInfo
from models.distributor.product.product_info import ProductInfo

customer_order_blueprint = Blueprint('customer_order_blueprint', __name__)
session =  db_connection()

# TODO: Categorise the functionality into different functions and services and modularize the code, also add validation for the request body, add error handling and logging for each API
# Test the APIs using Postman and Swagger, also add unit tests for each API, also add API documentation, have 2 weeks of time to complete whole project

@customer_order_blueprint.route('/orders', methods=['GET'])
def order_details():
    orders_data = CustomerOrder.query.count()
    return jsonify(status=200, success=True, data=orders_data), 200

# create order
@customer_order_blueprint.route('/order/create', methods=['POST'])
def create_order():
    # TODO: Add validation for the request body
    order_details = request.get_json()
    customer_id = order_details.get('customerId')
    address_id = order_details.get('addressId')
    selected_date = order_details.get('selectedDate')
    selected_slot = order_details.get('selectedSlot')
    special_instruction = order_details.get('specialInstruction')
    order_items = order_details.get('orderItems')
    payment_method = order_details.get('paymentMethod')

    # fetch nearest distributor for the address, find the cosign distance between distributor and customer address, first find the latitude and longitude of the address, then find the nearest distributor
    customer_address = CustomerAddress.query.filter_by(id=address_id).first()
    customer_latitude = customer_address.latitude
    customer_longitude = customer_address.longitude

    # write sql query to find the nearest distributor from the customer address within 1.5 km radius
    nearest_distributor_query = (
        DistributorInfo.query
        .filter(
            func.ST_DWithin(
                DistributorInfo.location,
                func.ST_SetSRID(ST_Point(customer_longitude, customer_latitude), 4326),
                1500
            )
        )
        .order_by(
            func.ST_Distance(
                DistributorInfo.location,
                func.ST_SetSRID(ST_Point(customer_longitude, customer_latitude), 4326)
            )
        )
        .limit(1)
    )

    nearest_distributor = nearest_distributor_query.first()

    if not nearest_distributor:
        return jsonify(status=400, success=False, data="No distributor found for the address"), 400

    # check if payment method is PAY_LATER, PAY_NOW, CASH_ON_DELIVERY
    if payment_method == 'PAY_LATER':
        pay_later = True
        status = 'ORDER_PLACED'
    elif payment_method == 'PAY_NOW':
        pay_later = False
        status = 'INITIATED'
    elif payment_method == 'CASH_ON_DELIVERY':
        pay_later = False
        status = 'ORDER_PLACED'
    else:
        return jsonify(status=400, success=False, data="Invalid payment method"), 400
    
    # add order to database
    new_order = CustomerOrder(customer_id=customer_id, address_id=address_id, distributor_id=nearest_distributor.id, selected_date=selected_date, selected_slot=selected_slot, status=status, special_instruction=special_instruction, is_paid=False, pay_later=pay_later)
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    # add order items
    for item in order_items:
        product_id = item.get('productId')
        quantity = item.get('quantity')
        product_data = session.query(ProductInfo).filter_by(id=product_id).first()
        new_order_item = CustomerOrderItem(order_id=new_order.id, product_id=product_id, quantity=quantity, price=product_data.price)
        session.add(new_order_item)
        session.commit()
    
    # add order payment
    if payment_method == 'PAY_NOW':
        transaction_id = f"txn_order_{new_order.id}"
        amount = order_details.get('totalAmount')
        new_order_payment = CustomerOrderPayment(order_id=new_order.id, status='INITIATED', gateway_payment_id=transaction_id, amount=amount, currency='INR', attempts=0)
        session.add(new_order_payment)
        session.commit()

        # initiate payment gateway
        # payment_gateway_response = initiate_payment_gateway(transaction_id, amount)
    elif payment_method == 'CASH_ON_DELIVERY':
        transaction_id = f"txn_cod_{new_order.id}"
        amount = order_details.get('totalAmount')
        new_order_payment = CustomerOrderPayment(order_id=new_order.id, status='CASH_ON_DELIVERY', gateway_payment_id=transaction_id, amount=amount, currency='INR', attempts=0)
        session.add(new_order_payment)
        session.commit()
    elif payment_method == 'PAY_LATER':
        transaction_id = f"txn_pay_later_{new_order.id}"
        amount = order_details.get('totalAmount')
        new_order_payment = CustomerOrderPayment(order_id=new_order.id, status='PAY_LATER', gateway_payment_id=transaction_id, amount=amount, currency='INR', attempts=0)
        session.add(new_order_payment)
        session.commit()
    
    session.close()
    response = {
        'order_details': new_order,
        'order_items': order_items,
        'order_payment': new_order_payment
    }
    return jsonify(status=200, success=True, data=response), 200

# get order by id
@customer_order_blueprint.route('/orders/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    order_data = CustomerOrder.query.filter_by(id=order_id).first()
    return jsonify(status=200, success=True, data=order_data), 200

# get all orders
@customer_order_blueprint.route('/orders', methods=['GET'])
def get_all_orders():
    orders_data = CustomerOrder.query.all()
    return jsonify(status=200, success=True, data=orders_data), 200

# get orders by customer id for which payment done or paylater True
@customer_order_blueprint.route('/orders/<int:customer_id>', methods=['GET'])
def get_orders_by_customer_id(customer_id):
    allowed_statuses = ['PAID', 'PAY_LATER', 'CASH_ON_DELIVERY', 'ORDER_PLACED']
    orders_data = session.query(CustomerOrder,CustomerOrderPayment).join(CustomerOrderPayment, CustomerOrder.id == CustomerOrderPayment.order_id).filter(and_(CustomerOrder.customer_id == customer_id, or_(CustomerOrderPayment.status.in_(allowed_statuses), CustomerOrder.pay_later == True, CustomerOrder.is_paid == True))).all()
    session.close()

    return jsonify(status=200, success=True, data=orders_data), 200

# calculate total amount of order
@customer_order_blueprint.route('/orders/total', methods=['POST'])
def calculate_total_amount():
    order_details = request.get_json()
    order_items = order_details.get('orderItems')
    address_id = order_details.get('addressId')
    item_total = 0

    lift_available = CustomerAddress.query.filter_by(id=address_id).first().lift_available
    delivery_charge = 0

    # fetch product details from product table and calculate total amount
    for item in order_items:
        product_id = item.get('productId')
        quantity = item.get('quantity')
        product_data = session.query(ProductInfo).filter_by(id=product_id).first()
        item_total += product_data.price * quantity
        delivery_charge += quantity * 2
    
    delivery_charge = delivery_charge if not lift_available else 0
    taxes = 0
    total_amount = item_total + delivery_charge + taxes 
    
    response = {
        'itemTotal': item_total,
        'deliveryCharge': delivery_charge,
        'totalAmount': total_amount
    }

    return jsonify(status=200, success=True, data=response), 200

# update order payment status
@customer_order_blueprint.route('/orders/payment/update', methods=['PUT'])
def update_order_payment_status():
    order_payment_details = request.get_json()
    order_id = order_payment_details.get('orderId')
    status = order_payment_details.get('status')
    transaction_id = order_payment_details.get('transactionId')

    # validate status from payment gateway for the transaction id
    # payment_gateway_response = validate_payment_gateway(transaction_id)

    # if yes, update the status in the database
    payment_data = CustomerOrderPayment.query.filter_by(transaction_id=transaction_id).first()
    if not payment_data:
        return jsonify(status=400, success=False, data="Invalid transaction id"), 400
    
    if payment_data.order_id != order_id:
        return jsonify(status=400, success=False, data="Invalid order id"), 400

    payment_data.status = status

    # update order status if payment is successful
    if status == 'PAID':
        order_data = CustomerOrder.query.filter_by(id=order_id).first()
        order_data.status = 'ORDER_PLACED'
        session.commit()

    session.commit()
    session.close()

    response = {
        'orderId': order_id,
        'status': status
    }
    return jsonify(status=200, success=True, data=response), 200

# order status update
@customer_order_blueprint.route('/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    order_details = request.get_json()
    status = order_details.get('status')
    order_data = CustomerOrder.query.filter_by(id=order_id).first()
    order_data.status = status
    session.commit()
    session.close()

    response = {
        'orderId': order_id,
        'status': status
    }
    return jsonify(status=200, success=True, data=response), 200
