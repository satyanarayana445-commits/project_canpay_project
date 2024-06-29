from flask import jsonify, request, Blueprint

customer_address_details_blueprint = Blueprint('customer_address_details_blueprint', __name__)


@customer_address_details_blueprint.route('/customer_address', methods=['GET'])
def customer_address_details():
    return jsonify(status=200, success=True, message="success"), 200