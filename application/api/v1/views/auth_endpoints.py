'''auth_endpoints.py contains endpoints for register,login and logout'''
import random

import re
from flask import Flask, request, jsonify, Blueprint, make_response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt)
from ..models import auth_models
from ..utils import list_iterator

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

BLACKLIST = set()
user_object = auth_models.Users()


@auth.route('/register', methods=['POST'])
def register():
    '''endpoint to add  a new user'''
    data = request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"}), 400
    username = data.get('username').strip()
    name = data.get('name')
    email = data.get('email').strip()
    password = data.get('password').strip()
    confirm_password = data.get('confirm_password').strip()
    role = data.get('role').lower().strip()
    roles = ["admin", "attendant"]
    if role not in roles:
        return jsonify({"message": "The role {} does not exist.Only admin and attendant roles are allowed".format(role)}), 400

    userinfo = [username, name, role, password, confirm_password, email]

    exists = list_iterator(userinfo)
    if exists is False:
        return jsonify({"message": "Make sure all fields have been filled out"}), 206
    if len(password) < 4:
        return jsonify({"message": "The password is too short,minimum length is 4"}), 400
    if confirm_password != password:
        return jsonify({"message": "The passwords you entered don't match"}), 400
    match = re.match(
        r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match is None:
        return jsonify({"message": "Enter a valid email address"}), 403
    response = jsonify(user_object.put(name, username, email, password, role))
    response.status_code = 201
    return response


@auth.route('/login', methods=['POST'])
def login():
    '''login user by verifying password and creating an access token'''
    data = request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"}), 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"message": "Username or password missing"}), 206
    authorize = user_object.verify_password(username, password)
    user = user_object.get_user_by_username(username)
    if authorize == "True":
        access_token = create_access_token(identity=user)
        return jsonify(dict(token=access_token, message="Login successful!")), 200

    response = jsonify(authorize)
    response.status_code = 401
    return response


@auth.route('/logout', methods=['POST'])
@jwt_required
def logout():
    '''logout user by revoking password'''
    json_token_identifier = get_raw_jwt()['jti']
    BLACKLIST.add(json_token_identifier)
    return jsonify({"message": "Successfully logged out"}), 200


@auth.route('/users', methods=['GET'])
def get_all_users():
    '''Endpoint to get all users'''

    response = make_response(jsonify(user_object.get_all_users()))
    response.status_code = 200
    return response


@auth.route('/users/<username>', methods=['GET'])
def get_user_by_username(username):
    '''Endpoint to get a  user by username'''
    response = make_response(
        jsonify(user_object.get_user_by_username(username)))
    response.status_code = 200
    return response
