import json
from .base_test import BaseTestCase

class TestRegister(BaseTestCase):

    def test_registration(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='chacha@gmail.com',
                    role='attendant',
                    username='chacha',
                    password='1234',
                    confirm_password='1234'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data)
            self.assertEqual("User with username chacha added successfully",response_data["message"])
            self.assertEqual(response.status_code, 201)

    def test_registration_with_invalid_email(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='chachagmail.com',
                    role='attendant',
                    username='chacha',
                    password='1234',
                    confirm_password='1234'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data)
            self.assertEqual("Enter a valid email address",response_data["message"])
            self.assertEqual(response.status_code, 403)

    def test_registration_if_user_already_exits(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='chacha@gmail.com',
                    role='attendant',
                    username='chacha',
                    password='1234',
                    confirm_password='1234'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data)
            print(response_data)
            self.assertEqual("Username already exists",response_data["message"])
            
    def test_user_login(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='chacha',
                    password='1234'
                    
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data)
            self.assertEqual("Login successful!",response_data["message"])
            self.assertEqual(response.status_code, 200)
    def test_user_logout(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='chacha',
                    password='1234'
                    
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data)
            token=response_data["token"]
            self.assertEqual("Login successful!",response_data["message"])
            self.assertEqual(response.status_code, 200)
            response2 = self.client.post(
                '/api/v1/auth/logout',headers=dict(Authorization="Bearer " + token))
            response_data2 = json.loads(response2.data)
            print (response_data2)
            self.assertEqual("Successfully logged out",response_data2["message"])
            self.assertEqual(response.status_code, 200)
    
