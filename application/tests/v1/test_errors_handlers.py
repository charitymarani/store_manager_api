import json
from .base_test import BaseTestCase


class TestErrors(BaseTestCase):
    def test_404(self):
        with self.client:
            response = self.client.get('/api/v1/charity')
            result = json.loads(response.data)
            self.assertEqual('Resource not found', result['error'])

    def test_400(self):
        with self.client:
            response = self.client.post('/api/v1/auth/register', data=json.dumps({
                "name":"charity",,
                "email": "chacha@gmail.com",
                "username": "cg",
                "password": "1234",
                "role": "attendant",
                "confirm_password": "1234",
            }), content_type='application/json')

            result = json.loads(response.data)
            self.assertEqual('Bad request', result['error'])
    def test_405(self):
        with self.client:
            response = self.client.get('/api/v1/auth/register', data=json.dumps({
                "name": "charity",
                "email": "chachk@gmail.com",
                "username": "ck",
                "password": "1234",
                "role": "attendant",
                "confirm_password": "1234",
            }), content_type='application/json')

            result = json.loads(response.data)
            self.assertEqual('Method not allowed', result['error'])
    def test_500(self):
        with self.client:
            response = self.client.post('/api/v1/auth/register', data=json.dumps({
                
                "password": "1234",
                "role": "attendant",
                "confirm_password": "1234"
            }), content_type='application/json')

            result = json.loads(response.data)
            self.assertEqual('Internal server error', result['error'])
