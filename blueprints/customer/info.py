from flask import jsonify, request, Blueprint

customer_info_details_blueprint = Blueprint('customer_info_details_blueprint', __name__)


@customer_info_details_blueprint.route('/customer_info', methods=['GET'])
def customer_info_details():
    return jsonify(status=200, success=True, message="success"), 200