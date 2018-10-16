import json
from .base_test import BaseTestCase
class TestSales(BaseTestCase):

    def test_post_sales(self):
        '''Only an attendant can post sales'''
        with self.client:
            # Register an attendant
            self.client.post(
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
        
            # login the attendant
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
                '/api/v1/sales',headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict(
                    items_count=4,
                    total_amount=5000
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data)
            print(response_data)
            
            self.assertEqual("A sale has been created successfully",response_data["message"])
            self.assertEqual(response.status_code, 201)

    