import string
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils import get_item_by_key

USERS_DICT = {}

class Users():
    '''class to represent users model'''
       

    def put(self, name, username, email, password,role):
        '''add a user to USERS_DICT'''
        self.oneuser_dict = {}
        if username in USERS_DICT:
            return {"message":"Username already exists,try a different one!"}
        
        self.oneuser_dict["name"] = name
        self.oneuser_dict["email"] = email
        self.oneuser_dict["username"] = username
        self.oneuser_dict["role"] = role
        pw_hash = generate_password_hash(password)
        self.oneuser_dict["password"] = pw_hash

        USERS_DICT[username] = self.oneuser_dict
        return {"message":"User with username {} added successfully".format(username)}

    def verify_password(self, username, password):
        '''verify the password a user enters while logging in'''
        if username in USERS_DICT:
            result = check_password_hash(USERS_DICT[username]["password"], password)
            if result is True:
                return "True"
            return {"message": "The password you entered is incorrect"}
        return {"message": "Username does not exist in our records"}
    def get_user_by_username(self,username):
        result=get_item_by_key(username,USERS_DICT)
        if result is False:
            return {"message":"User not found"}
        return result
    def get_all_users(self):
        return USERS_DICT