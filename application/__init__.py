
'''application/apps.py'''
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from instance.config import app_config
from .api.v1.views.auth_endpoints import auth, BLACKLIST
from .api.v1.views.products_endpoints import product
from .api.v1.views.sales_endpoints import sale


def create_app(config):
    '''function configuring the Flask App'''
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config])
    app.config["TESTING"] = True

    app.config['JWT_SECRET_KEY'] = 'mysecretkey'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_claims_to_access_token(user_object):
        '''add role claims to access token'''
        return {'role': user_object['role']}

    @jwt.user_identity_loader
    def user_identity_lookup(user_object):
        '''set token identity from user_object passed to username'''
        return user_object["username"]

    @jwt.token_in_blacklist_loader
    def check_if_token_blacklist(decrypted_token):
        '''check if jti(unique identifier) is in black list'''
        json_token_identifier = decrypted_token['jti']
        return json_token_identifier in BLACKLIST

    '''Error handlers'''
    @app.errorhandler(400)
    def bad_request(error):
        '''error handler for Bad request'''
        return jsonify(dict(error='Bad request')), 400

    @app.errorhandler(404)
    def Resource_not_found(error):
        '''error handler for 404'''
        return jsonify(dict(error='Resource not found')), 404

    @app.errorhandler(405)
    def unauthorized(error):
        '''error handler for 405'''
        return jsonify(dict(error='Method not allowed')), 405

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        return jsonify(dict(error='Internal server error')), 500

    app.register_blueprint(auth)
    app.register_blueprint(product)
    app.register_blueprint(sale)

    return app
