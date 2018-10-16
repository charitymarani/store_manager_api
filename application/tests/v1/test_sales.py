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
           
            
            self.assertEqual("A sale has been created successfully",response_data["message"])
            self.assertEqual(response.status_code, 201)

    def test_get_all_sales(self):
        '''Only an admin can view all sales records'''
        with self.client:
            #register an admin and an attendant
            self.client.post('/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='chacha@gmail.com',
                    role='attendant',
                    username='chachatt',
                    password='1234',
                    confirm_password='1234'
                    )),
                    content_type='application/json'
                    )
            self.client.post('/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='chacha@gmail.com',
                    role='admin',
                    username='chadmin',
                    password='1234',
                    confirm_password='1234'
                    )),
                    content_type='application/json'
                    )
            response_login_attendant=self.client.post('api/v1/auth/login',
                data=json.dumps(dict(
                    username="chachatt",
                    password="1234"
                )),
                content_type='application/json'
                )
            result_login_attendant=json.loads(response_login_attendant.data)
            token1=result_login_attendant["token"]
            #  login admin
            response_login_admin=self.client.post('api/v1/auth/login',
                data=json.dumps(dict(
                    username="chadmin",
                    password="1234"
                )),
                content_type='application/json'
                )
            result_login_admin=json.loads(response_login_admin.data)
            token2=result_login_admin["token"]
            #let attendant post a sale
            self.client.post(
                '/api/v1/sales',headers=dict(Authorization="Bearer " + token1),
                data=json.dumps(dict(
                    items_count=4,
                    total_amount=5000
                )),
                content_type='application/json'
            )
            #Let admin get all sales
            response=self.client.get('api/v1/sales',headers=dict(Authorization="Bearer " + token2))
            
            self.assertEqual(response.status_code,200)

    def test_get_sale_by_id(self):
        with self.client:
            #register an admin and an attendant
            self.client.post('/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='chacha@gmail.com',
                    role='attendant',
                    username='anattendant',
                    password='1234',
                    confirm_password='1234'
                    )),
                    content_type='application/json'
                    )
            self.client.post('/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='chacha@gmail.com',
                    role='admin',
                    username='anadmin',
                    password='1234',
                    confirm_password='1234'
                    )),
                    content_type='application/json'
                    )
            response_login_attendant=self.client.post('api/v1/auth/login',
                data=json.dumps(dict(
                    username="anattendant",
                    password="1234"
                )),
                content_type='application/json'
                )
            result_login_attendant=json.loads(response_login_attendant.data)
            token1=result_login_attendant["token"]
            #  login admin
            response_login_admin=self.client.post('api/v1/auth/login',
                data=json.dumps(dict(
                    username="anadmin",
                    password="1234"
                )),
                content_type='application/json'
                )
            result_login_admin=json.loads(response_login_admin.data)
            token2=result_login_admin["token"]
            #let attendant post a sale
            self.client.post(
                '/api/v1/sales',headers=dict(Authorization="Bearer " + token1),
                data=json.dumps(dict(
                    items_count=4,
                    total_amount=5000
                )),
                content_type='application/json'
            )
            #let the attendant who posted get the sale
            responseatt=self.client.get('api/v1/sales',headers=dict(Authorization="Bearer " + token1))
            
            self.assertEqual(responseatt.status_code,200)
            #let the admin  get the sale
            responseadmin=self.client.get('api/v1/sales',headers=dict(Authorization="Bearer " + token2))
            
            self.assertEqual(responseadmin.status_code,200)
    
    
