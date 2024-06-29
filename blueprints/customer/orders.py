from flask import jsonify,request, Blueprint
from sqlalchemy import and_, or_
from db_conn.db import db_connection
from models.customer.order.customer_order import CustomerOrder
from models.customer.order.customer_order_item import CustomerOrderItem
from models.customer.order.customer_order_payment import CustomerOrderPayment
from models.distributor.product.product_info import ProductInfo

app = Blueprint('customer_order_blueprint', __name__)
session =  db_connection()


@app.route('/orders', methods=['GET'])
def order_details():
    orders_data = CustomerOrder.query.count()
    return jsonify(status=200, success=True, data=orders_data), 200

# create order
@app.route('/order/create', methods=['POST'])
def create_order():
    # TODO: Add validation for the request body
    order_details = request.get_json()
    address_id = order_details.get('addressId')
    selected_date = order_details.get('selectedDate')
    selected_slot = order_details.get('selectedSlot')
    special_instruction = order_details.get('specialInstruction')
    order_items = order_details.get('orderItems')
    payment_method = order_details.get('paymentMethod')

    # check if payment method is PAY_LATER, PAY_NOW, CASH_ON_DELIVERY
    if payment_method == 'PAY_LATER':
        is_paid = False
        pay_later = True
    elif payment_method == 'PAY_NOW':
        is_paid = True
        pay_later = False
    elif payment_method == 'CASH_ON_DELIVERY':
        is_paid = False
        pay_later = False
    else:
        return jsonify(status=400, success=False, data="Invalid payment method"), 400
    
    # create order
    new_order = CustomerOrder(address_id=address_id, selected_date=selected_date, selected_slot=selected_slot, special_instruction=special_instruction, is_paid=is_paid, pay_later=pay_later)
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    # create order items
    for item in order_items:
        product_id = item.get('productId')
        quantity = item.get('quantity')
        product_data = session.query(ProductInfo).filter_by(id=product_id).first()
        new_order_item = CustomerOrderItem(order_id=new_order.id, product_id=product_id, quantity=quantity, price=product_data.price)
        session.add(new_order_item)
        session.commit()
    
    # create order payment
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
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    order_data = CustomerOrder.query.filter_by(id=order_id).first()
    return jsonify(status=200, success=True, data=order_data), 200

# get all orders
@app.route('/orders', methods=['GET'])
def get_all_orders():
    orders_data = CustomerOrder.query.all()
    return jsonify(status=200, success=True, data=orders_data), 200

# get orders by customer id for which payment done or paylater True
@app.route('/orders/<int:customer_id>', methods=['GET'])
def get_orders_by_customer_id(customer_id):
    allowed_payment_methods = ['PAID', 'PAY_LATER', 'CASH_ON_DELIVERY']
    orders_data = session.query(CustomerOrder,CustomerOrderPayment).join(CustomerOrderPayment, CustomerOrder.id == CustomerOrderPayment.order_id).filter(and_(CustomerOrder.customer_id == customer_id, or_(CustomerOrderPayment.status.in_(allowed_payment_methods), CustomerOrder.pay_later == True, CustomerOrder.is_paid == True))).all()
    session.close()

    return jsonify(status=200, success=True, data=orders_data), 200

# calculate total amount of order
@app.route('/orders/total', methods=['POST'])
def calculate_total_amount():
    order_details = request.get_json()
    order_items = order_details.get('orderItems')
    total = 0

    # fetch product details from product table and calculate total amount
    for item in order_items:
        product_id = item.get('productId')
        quantity = item.get('quantity')
        product_data = session.query(ProductInfo).filter_by(id=product_id).first()
        total += product_data.price * quantity

    return jsonify(status=200, success=True, data=total), 200

