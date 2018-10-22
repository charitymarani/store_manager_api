import string
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils import get_item_by_key, get_all

USERS_DICT = []


class Users():
    '''class to represent users model'''

    def put(self, name, username, email, password, role):
        '''add a user to USERS_DICT'''
        self.oneuser_dict = {}

        email_data = get_item_by_key("email", email, USERS_DICT)
        username_data = get_item_by_key("username", username, USERS_DICT)
        if "message" not in email_data:
            return {"message": "Email already in use,try a different one!"}
        if "message" not in username_data:
            return {"message": "Username already taken, try a different one"}

        self.oneuser_dict["name"] = name
        self.oneuser_dict["email"] = email
        self.oneuser_dict["username"] = username
        self.oneuser_dict["role"] = role
        pw_hash = generate_password_hash(password)
        self.oneuser_dict["password"] = pw_hash

        USERS_DICT.append(self.oneuser_dict)
        return {"message": "User with username {} added successfully".format(username)}

    def verify_password(self, username, password):
        '''verify the password a user enters while logging in'''
        user_obj = get_item_by_key('username', username, USERS_DICT)
        if "message" not in user_obj:
            result = check_password_hash(
                user_obj['password'], password)
            if result is True:
                return "True"
            return {"message": "The password you entered is incorrect"}
        return user_obj

    def get_user_by_username(self, username):
        result = get_item_by_key('username', username, USERS_DICT)
        return result

    def get_all_users(self):
        result = get_all(USERS_DICT)
        return result
