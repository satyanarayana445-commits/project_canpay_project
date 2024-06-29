from flask import jsonify, Blueprint
from models.customer.order.customer_order import Orders

order_details_blueprint = Blueprint('order_details_blueprint', __name__)


@order_details_blueprint.route('/orders', methods=['GET'])
def order_details():
    orders_data = Orders.query.count()
    print("order_count", orders_data)
    return jsonify(status=200, success=True, data="orders_data"), 200