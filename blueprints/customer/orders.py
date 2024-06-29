from flask import jsonify, request, Blueprint

order_details_blueprint = Blueprint('order_details_blueprint', __name__)


@order_details_blueprint.route('/orders', methods=['GET'])
def order_details():
    return jsonify(status=200, success=True, message="success"), 200