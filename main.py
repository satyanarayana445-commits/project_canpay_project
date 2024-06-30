from flask import Flask
from flask_cors import CORS
from controllers.customer.customer_info import customer_info_blueprint
from controllers.customer.customer_order import customer_order_blueprint
from controllers.delivery_agent.delivery_agent_info import delivery_info_blueprint
from controllers.delivery_agent.delivery_agent_order import delivery_agent_order_blueprint
from controllers.distributor.distributor_info import distributor_info_blueprint
from controllers.distributor.customer_order import distributor_customer_order_blueprint
from controllers.distributor.delivery_agent_info import distributor_delivery_agent_info_blueprint
from db_conn import db
from database_uri import database_uri



def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['CACHE_TYPE'] = 'simple'
    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    app.config['CSRF_ENABLED'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri()
    app.config['CSRF_ENABLED'] = True
    db.init_app(app)
    app.register_blueprint(customer_info_blueprint, url_prefix='/customer')
    app.register_blueprint(customer_order_blueprint, url_prefix='/customer/order')
    app.register_blueprint(delivery_info_blueprint, url_prefix='/delivery_agent')
    app.register_blueprint(delivery_agent_order_blueprint, url_prefix='/delivery_agent/order')
    app.register_blueprint(distributor_info_blueprint, url_prefix='/distributor')
    app.register_blueprint(distributor_customer_order_blueprint, url_prefix='/distributor/order')
    app.register_blueprint(distributor_delivery_agent_info_blueprint, url_prefix='/distributor/delivery_agent')
    return app


if __name__ == "__main__":
    create_app().run()
    # create_app().run(debug=True, host="0.0.0.0", port=80, use_reloader=False)

