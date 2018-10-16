'''application/apps.py'''
from flask import Flask
from flask_jwt_extended import JWTManager

from instance.config import app_config
from .api.v1.views.auth_endpoints import auth,BLACKLIST
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
        print(user_object)
        return user_object["username"]

    @jwt.token_in_blacklist_loader
    def check_if_token_blacklist(decrypted_token):
        '''check if jti(unique identifier) is in black list'''
        json_token_identifier = decrypted_token['jti']
        return json_token_identifier in BLACKLIST

    app.register_blueprint(auth)
    app.register_blueprint(product)
    app.register_blueprint(sale)

    return app
