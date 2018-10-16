import json
from .base_test import BaseTestCase
class TestProducts(BaseTestCase):

    def test_post_product(self):
        '''Only an admin can post products'''
        with self.client:
            # Register an admin user
            register_response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='chacha@gmail.com',
                    role='admin',
                    username='chacha',
                    password='1234',
                    confirm_password='1234'
                )),
                content_type='application/json'
            )
            # login as admin
            login_response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='chacha',
                    password='1234'
                    
                )),
                content_type='application/json'
            )
            result=json.loads(login_response.data)
            token=result["token"]
            response = self.client.post(
                '/api/v1/products',headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict(
                    id=100,
                    name='chunky heels',
                    category='shoes',
                    purchase_price=1000,
                    selling_price=1800,
                    quantity=70,
                    low_limit=10,
                    description='A wide based heel'

                )),
                content_type='application/json'
                
            )
            response_data = json.loads(response.data)
            self.assertEqual("Product with id 100 added successfully",response_data["message"])
            self.assertEqual(response.status_code, 201)

    def test_get_all_products(self):
        with self.client:
            # Register a user
            register_response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='chacha@gmail.com',
                    role='admin',
                    username='chacha',
                    password='1234',
                    confirm_password='1234'
                )),
                content_type='application/json'
            )
        
            # login a user
            login_response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='chacha',
                    password='1234'
                    
                )),
                content_type='application/json'
            )
            result=json.loads(login_response.data)
            token=result["token"]
            response = self.client.get(
                '/api/v1/products',headers=dict(Authorization="Bearer " + token))
            response_data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
    