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
                    name="charity marani",
                    email="chachat@gmail.com",
                    role="attendant",
                    username="chacha1",
                    password="1234",
                    confirm_password="1234"
                )),
                content_type='application/json'
            )
            # Register admin
            self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name="charity marani",
                    email="cha@gmail.com",
                    role="admin",
                    username="chachatheadmin",
                    password="1234",
                    confirm_password="1234"
                )),
                content_type='application/json'
            )
            # login admin
            login_admin_response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username="chachatheadmin",
                    password="1234"

                )),
                content_type='application/json'
            )
            resultadmin = json.loads(login_admin_response.data)

            tokenadmin = resultadmin["token"]

            # login the attendant
            login_response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username="chacha1",
                    password="1234"

                )),
                content_type='application/json'
            )
            result = json.loads(login_response.data)

            token = result["token"]
            # Test successful post of a sale
            response = self.client.post(
                '/api/v1/sales', headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict(
                    items_count=4,
                    total_amount=5000
                )),
                content_type='application/json'
            )

            response_data = json.loads(response.data)
            self.assertEqual(
                "A sale has been created successfully", response_data["message"])
            self.assertEqual(response.status_code, 201)
            # Test admin can't post a sale
            responsec = self.client.post(
                '/api/v1/sales', headers=dict(Authorization="Bearer " + tokenadmin),
                data=json.dumps(dict(
                    items_count=4,
                    total_amount=5000
                )),
                content_type='application/json'
            )

            response_datac = json.loads(responsec.data)
            self.assertEqual(
                "Only an attendant is permitted to post sales", response_datac["message"])
            self.assertEqual(responsec.status_code, 401)
            # Test sale data can't be empty
            responsed = self.client.post(
                '/api/v1/sales', headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict()
                                ),
                content_type='application/json'
            )
            response_datad = json.loads(responsed.data)
            self.assertEqual("Fields cannot be empty",
                             response_datad["message"])
            self.assertEqual(responsed.status_code, 400)
            # Test some missing fields
            responsee = self.client.post(
                '/api/v1/sales', headers=dict(Authorization="Bearer " + token),
                data=json.dumps(dict(
                    items_count="",
                    total_amount=5000
                )),
                content_type='application/json'
            )

            response_datae = json.loads(responsee.data)
            self.assertEqual(
                "Items_count and total_amount fields can't be empty", response_datae["message"])
            self.assertEqual(responsee.status_code, 206)

    def test_get_all_sales(self):
        '''Only an admin can view all sales records'''
        with self.client:
            # register an admin and an attendant
            self.client.post('/api/v1/auth/register',
                             data=json.dumps(dict(
                                 name="charity marani",
                                 email="cherry@gmail.com",
                                 role="attendant",
                                 username="chachatt",
                                 password="1234",
                                 confirm_password="1234"
                             )),
                             content_type='application/json'
                             )
            self.client.post('/api/v1/auth/register',
                             data=json.dumps(dict(
                                 name="charity marani",
                                 email="roy@gmail.com",
                                 role="admin",
                                 username="chadmin",
                                 password="1234",
                                 confirm_password="1234"
                             )),
                             content_type='application/json'
                             )
            response_login_attendant = self.client.post('api/v1/auth/login',
                                                        data=json.dumps(dict(
                                                            username="chachatt",
                                                            password="1234"
                                                        )),
                                                        content_type='application/json'
                                                        )
            result_login_attendant = json.loads(response_login_attendant.data)
            token1 = result_login_attendant["token"]
            #  login admin
            response_login_admin = self.client.post('api/v1/auth/login',
                                                    data=json.dumps(dict(
                                                        username="chadmin",
                                                        password="1234"
                                                    )),
                                                    content_type='application/json'
                                                    )
            result_login_admin = json.loads(response_login_admin.data)
            token2 = result_login_admin["token"]
            # let attendant post a sale
            self.client.post(
                '/api/v1/sales', headers=dict(Authorization="Bearer " + token1),
                data=json.dumps(dict(
                    items_count=4,
                    total_amount=5000
                )),
                content_type='application/json'
            )
            # Let admin get all sales
            response = self.client.get(
                'api/v1/sales', headers=dict(Authorization="Bearer " + token2))
            self.assertEqual(response.status_code, 200)
            # Test admin is not allowed to view all sales
            responseb = self.client.get(
                'api/v1/sales', headers=dict(Authorization="Bearer " + token1))
            responseb_data = json.loads(responseb.data)
            self.assertEqual(
                "Only an admin can view all sales records", responseb_data["message"])
            self.assertEqual(responseb.status_code, 401)

    def test_get_empty_sales_record(self):
        with self.client:
            self.client.post('/api/v1/auth/register',
                             data=json.dumps(dict(
                                 name="charity marani",
                                 email="chachad@gmail.com",
                                 role="admin",
                                 username="betty",
                                 password="1234",
                                 confirm_password="1234"
                             )),
                             content_type='application/json'
                             )
            response_login = self.client.post('api/v1/auth/login',
                                              data=json.dumps(dict(
                                                  username="betty",
                                                  password="1234"
                                              )),
                                              content_type='application/json'
                                              )
            result_login = json.loads(response_login.data)
            token3 = result_login["token"]
            results = self.client.get(
                '/api/v1/sales', headers=dict(Authorization="Bearer " + token3))
            results_data = json.loads(results.data)
            print(results_data)
            self.assertEqual("There are no records", results_data["message"])

    def test_get_sale_by_id(self):
        with self.client:
            # register an admin and two attendants
            self.client.post('/api/v1/auth/register',
                             data=json.dumps(dict(
                                 name='charity marani',
                                 email='niki@gmail.com',
                                 role='attendant',
                                 username='myattendant',
                                 password='1234',
                                 confirm_password='1234'
                             )),
                             content_type='application/json'
                             )
            self.client.post('/api/v1/auth/register',
                             data=json.dumps(dict(
                                 name='charity marani',
                                 email='joy@gmail.com',
                                 role='admin',
                                 username='myadmin',
                                 password='1234',
                                 confirm_password='1234'
                             )),
                             content_type='application/json'
                             )
            self.client.post('/api/v1/auth/register',
                             data=json.dumps(dict(
                                 name='charity marani',
                                 email='joel@gmail.com',
                                 role='attendant',
                                 username='myattendant2',
                                 password='1234',
                                 confirm_password='1234'
                             )),
                             content_type='application/json'
                             )
            # login attendant 1
            response_login_attendant = self.client.post('api/v1/auth/login',
                                                        data=json.dumps(dict(
                                                            username="myattendant",
                                                            password="1234"
                                                        )),
                                                        content_type='application/json'
                                                        )
            result_login_attendant = json.loads(response_login_attendant.data)
            a_token = result_login_attendant['token']
            # login attendant2
            response_login_attendant2 = self.client.post('api/v1/auth/login',
                                                         data=json.dumps(dict(
                                                             username="myattendant2",
                                                             password="1234"
                                                         )),
                                                         content_type='application/json'
                                                         )
            result_login_attendant2 = json.loads(
                response_login_attendant2.data)
            a_token1 = result_login_attendant2['token']

            #  login admin
            response_login_admin = self.client.post('api/v1/auth/login',
                                                    data=json.dumps(dict(
                                                        username='myadmin',
                                                        password='1234'
                                                    )),
                                                    content_type='application/json'
                                                    )
            result_login_admin = json.loads(response_login_admin.data)

            a_token2 = result_login_admin["token"]
            # let attendant post a sale
            self.client.post('/api/v1/sales',
                             headers=dict(Authorization="Bearer " + a_token),
                             data=json.dumps(dict(
                                 items_count=4,
                                 total_amount=5000
                             )),
                             content_type='application/json'
                             )
            # let the attendant who posted get the sale
            responseatt = self.client.get(
                'api/v1/sales/1', headers=dict(Authorization="Bearer " + a_token))

            self.assertEqual(responseatt.status_code, 200)
            # let the admin  get the sale
            responseadmin = self.client.get(
                'api/v1/sales/1', headers=dict(Authorization="Bearer " + a_token2))
            self.assertEqual(responseadmin.status_code, 200)
            # Test another attendant can't get a sale they didn't post
            responseatt2 = self.client.get(
                'api/v1/sales/1', headers=dict(Authorization="Bearer " + a_token1))
            resultatt2 = json.loads(responseatt2.data)
            self.assertEqual(
                "Only an admin or attendant who created this sale are allowed to view it", resultatt2["message"])
            self.assertEqual(responseatt2.status_code, 401)
            # Test get sale that does not exist
            responseadminz = self.client.get(
                'api/v1/sales/90', headers=dict(Authorization="Bearer " + a_token2))
            resultadminz = json.loads(responseadminz.data)
            self.assertEqual(
                "sale_id does not exist in our records", resultadminz["message"])
