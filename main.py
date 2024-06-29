from flask import Flask
from flask_cors import CORS
from blueprints.customer.info import customer_info_details_blueprint
from blueprints.customer.address import customer_address_details_blueprint
from blueprints.customer.orders import order_details_blueprint



def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['CACHE_TYPE'] = 'simple'
    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    app.config['CSRF_ENABLED'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['CSRF_ENABLED'] = True
    app.register_blueprint(customer_info_details_blueprint)
    app.register_blueprint(customer_address_details_blueprint)
    app.register_blueprint(order_details_blueprint)
    return app


if __name__ == "__main__":
    create_app().run()
    # create_app().run(debug=True, host="0.0.0.0", port=80, use_reloader=False)

