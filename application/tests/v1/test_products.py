import json
from .base_test import BaseTestCase


class TestProducts(BaseTestCase):

    def test_post_product(self):
        '''Only an admin can post products'''
        with self.client:
            # Register an admin user
            self.client.post(
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
            # Register attendant
            self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='chachat@gmail.com',
                    role='attendant',
                    username='jay',
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
            result = json.loads(login_response.data)
            token = result["token"]
            # Login attendant
            login_att_response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='jay',
                    password='1234'

                )),
                content_type='application/json'
            )
            resultatt = json.loads(login_att_response.data)
            tokenatt = resultatt["token"]
            # Test successful post
            response = self.client.post(
                '/api/v1/products', headers=dict(Authorization="Bearer " + token),
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
            self.assertEqual(
                "Product with id 100 added successfully", response_data["message"])
            self.assertEqual(response.status_code, 201)
            # Test post product with existing product id
            responsez = self.client.post(
                '/api/v1/products', headers=dict(Authorization="Bearer " + token),
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

            response_dataz = json.loads(responsez.data)
            self.assertEqual(
                "The product Id you entered is being used for another product", response_dataz["message"])
            self.assertEqual(response.status_code, 201)

            # Test empty data
            response1 = self.client.post(
                '/api/v1/products', headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict()
                                ),
                content_type='application/json'

            )
            response_data1 = json.loads(response1.data)
            self.assertEqual("Fields cannot be empty",
                             response_data1["message"])
            self.assertEqual(response1.status_code, 400)
            # Test missing required fields
            response2 = self.client.post(
                '/api/v1/products', headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict(
                    id="",
                    name="chunky",
                    category="shoes",
                    purchase_price=1000,
                    selling_price="",
                    quantity="",
                    low_limit="",
                    description="A wide based heel"

                )),
                content_type='application/json'

            )

            response_data2 = json.loads(response2.data)
            self.assertEqual("Some required fields are missing!",
                             response_data2["message"])
            self.assertEqual(response2.status_code, 206)
            # Test only admin can post products
            responseatt_post = self.client.post(
                '/api/v1/products', headers=dict(Authorization="Bearer " + tokenatt),
                data=json.dumps(dict(
                    id=200,
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

            response_data_att = json.loads(responseatt_post.data)
            self.assertEqual(
                "Only an admin is permitted to post products", response_data_att["message"])
            self.assertEqual(responseatt_post.status_code, 401)

    def test_get_all_products(self):
        with self.client:
            # Register a user
            self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='chach@gmail.com',
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
            result = json.loads(login_response.data)
            token = result["token"]
            response = self.client.get(

                '/api/v1/products', headers=dict(Authorization="Bearer " + token))
            self.assertEqual(response.status_code, 200)

    def test_empty_product_list(self):
        with self.client:
            self.client.post('/api/v1/auth/register',
                             data=json.dumps(dict(
                                 name="charity marani",
                                 email="chachadmin@gmail.com",
                                 role="admin",
                                 username="chachadmin",
                                 password="1234",
                                 confirm_password="1234"
                             )),
                             content_type='application/json'
                             )
            response_login = self.client.post('api/v1/auth/login',
                                              data=json.dumps(dict(
                                                  username="chachadmin",
                                                  password="1234"
                                              )),
                                              content_type='application/json'
                                              )
            result_login = json.loads(response_login.data)
            token2 = result_login["token"]
            result = self.client.get(
                '/api/v1/products', headers=dict(Authorization="Bearer " + token2))
            result_data = json.loads(result.data)
            self.assertEqual("There are no records", result_data["message"])

    def test_get_product_by_id(self):
        with self.client:
            # Register a user
            self.client.post(
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
            result = json.loads(login_response.data)
            token = result["token"]
            # Post a product
            self.client.post(
                '/api/v1/products', headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict(
                    id=300,
                    name='heels',
                    category='shoes',
                    purchase_price=1000,
                    selling_price=1800,
                    quantity=70,
                    low_limit=10,
                    description='A wide based heel'

                )),
                content_type='application/json'

            )
            # Test successful get product by id
            response = self.client.get(
                '/api/v1/products/300', headers=dict(Authorization="Bearer " + token))
            self.assertEqual(response.status_code, 200)
            # Test get product that doesn't exist
            response1 = self.client.get(
                '/api/v1/products/400', headers=dict(Authorization="Bearer " + token))
            resp = json.loads(response1.data)
            self.assertEqual(
                "product_id does not exist in our records", resp["message"])
