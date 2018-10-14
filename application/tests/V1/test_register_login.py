import json
from base_test import BaseTestCase

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
            self.assertEqual("User added successfully",response_data["message"])
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
            self.assertEqual("Invalid email",response_data["message"])
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
            self.assertEqual("User already exists",response_data["message"])
            self.assertEqual(response.status_code, 401)
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
    
