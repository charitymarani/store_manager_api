'''application/apps.py'''
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from instance.config import app_config

def create_app(config):
    '''function configuring the Flask App'''
    app = Flask(__name__)
    api = Api(app)

    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config])
    app.config["TESTING"] = True

    app.config['JWT_SECRET_KEY'] = 'mysecretkey'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    jwt = JWTManager(app)

    return app
