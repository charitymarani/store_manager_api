import json
from .base_test import BaseTestCase


class TestRegister(BaseTestCase):

    def test_registration(self):
        with self.client:
            # Test successful registration
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='caro@gmail.com',
                    role='attendant',
                    username='amina',
                    password='1234',
                    confirm_password='1234'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data)
            self.assertEqual(
                "User with username amina added successfully", response_data["message"])
            self.assertEqual(response.status_code, 201)

            # Test registration with nonexistent role

            response8 = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='key@gmail.com',
                    role='sWEEper',
                    username='key',
                    password='1234',
                    confirm_password='1234'
                )),
                content_type='application/json'
            )
            response_data8 = json.loads(response8.data)
            print(response_data8)
            self.assertEqual(response8.status_code, 400)
            self.assertEqual(
                "The role sweeper does not exist.Only admin and attendant roles are allowed", response_data8["message"])
            # Test registration with invalid email
            response2 = self.client.post(
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
            response_data2 = json.loads(response2.data)
            self.assertEqual("Enter a valid email address",
                             response_data2["message"])
            self.assertEqual(response2.status_code, 403)

            # test short password
            result = self.client.post('/api/v1/auth/register',
                                      content_type="application/json",
                                      data=json.dumps({"name": "marani", "username": "maro",
                                                       "email": "maro@gmail.com", "password": "123",
                                                       "confirm_password": "123", "role": "attendant"}))
            my_data = json.loads(result.data)
            self.assertEqual(result.status_code, 400)
            self.assertEqual(
                "The password is too short,minimum length is 4", my_data["message"])

            # test unmatching passwords
            result2 = self.client.post('/api/v1/auth/register',
                                       content_type="application/json",
                                       data=json.dumps({"name": "Mose", "username": "gebby",
                                                        "email": "gebby@to.cm", "password": "Test123",
                                                        "confirm_password": "Test13", "role": "attendant"}))
            my_data2 = json.loads(result2.data)
            self.assertEqual(result2.status_code, 400)
            self.assertEqual(
                "The passwords you entered don't match", my_data2["message"])
            # test for missing fields
            result3 = self.client.post('/api/v1/auth/register',
                                       content_type="application/json",
                                       data=json.dumps({"name": "", "username": "",
                                                        "email": "gebby@to.cm", "password": "Test123",
                                                        "confirm_password": "Test123", "role": "attendant"}))
            my_data3 = json.loads(result3.data)
            self.assertEqual(result3.status_code, 206)
            self.assertEqual(
                "Make sure all fields have been filled out", my_data3["message"])
            # Test for empty data
            result4 = self.client.post('/api/v1/auth/register',
                                       content_type="application/json",
                                       data=json.dumps({}))
            my_data4 = json.loads(result4.data)
            self.assertEqual(result4.status_code, 400)
            self.assertEqual("Fields cannot be empty", my_data4["message"])
            # Test registration using existing username
            response1 = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='hez@gmail.com',
                    role='attendant',
                    username='amina',
                    password='1234',
                    confirm_password='1234'
                )),
                content_type='application/json'
            )
            response_data1 = json.loads(response1.data)
            self.assertEqual(
                "Username already taken, try a different one", response_data1["message"])

    def test_existing_email(self):
        with self.client:
            # Register a user
            self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='jay@gmail.com',
                    role='attendant',
                    username='jayy',
                    password='1234',
                    confirm_password='1234'
                )),
                content_type='application/json'
            )
            # Test registration using existing email
            response2 = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='jay@gmail.com',
                    role='attendant',
                    username='jerry',
                    password='1234',
                    confirm_password='1234'
                )),
                content_type='application/json'
            )
            response_data2 = json.loads(response2.data)
            self.assertEqual(
                "Email already in use,try a different one!", response_data2["message"])

    def test_user_login(self):
        with self.client:
            # Register a user
            self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='mary@gmail.com',
                    role='attendant',
                    username='mary',
                    password='1234',
                    confirm_password='1234'
                )),
                content_type='application/json'
            )
            # Test for successful Login
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='mary',
                    password='1234'

                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data)
            self.assertEqual("Login successful!", response_data["message"])
            self.assertEqual(response.status_code, 200)
            # Test for empty data
            response2 = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict()
                                ),
                content_type='application/json'
            )
            response_data2 = json.loads(response2.data)
            self.assertEqual("Fields cannot be empty",
                             response_data2["message"])
            self.assertEqual(response2.status_code, 400)
            # Test for missing fields
            response3 = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='',
                    password='1234'

                )),
                content_type='application/json'
            )
            response_data3 = json.loads(response3.data)
            self.assertEqual("Username or password missing",
                             response_data3["message"])
            self.assertEqual(response3.status_code, 206)
            # Test for invalid login
            response4 = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='mary',
                    password='vbnc'

                )),
                content_type='application/json'
            )
            response_data4 = json.loads(response4.data)
            self.assertEqual(
                "The password you entered is incorrect", response_data4["message"])

            # Test for incorrect username
            response5 = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='ruth',
                    password='1234'

                )),
                content_type='application/json'
            )
            response_data5 = json.loads(response5.data)
            self.assertEqual(
                "username does not exist in our records", response_data5["message"])

    def test_user_logout(self):
        with self.client:
            # Register a user
            self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='mary@gmail.com',
                    role='attendant',
                    username='mary',
                    password='1234',
                    confirm_password='1234'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='mary',
                    password='1234'

                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data)
            token = response_data["token"]
            self.assertEqual("Login successful!", response_data["message"])
            self.assertEqual(response.status_code, 200)
            response2 = self.client.post(
                '/api/v1/auth/logout', headers=dict(Authorization="Bearer " + token))
            response_data2 = json.loads(response2.data)
            self.assertEqual("Successfully logged out",
                             response_data2["message"])
            self.assertEqual(response.status_code, 200)

    def test_get_all_users(self):
        # Register a user
        self.client.post(
            '/api/v1/auth/register',
            data=json.dumps(dict(
                name='charity marani',
                email='chacha@gmail.com',
                role='attendant',
                username='akinyi',
                password='1234',
                confirm_password='1234'
            )),
            content_type='application/json'
        )
        result = self.client.get('/api/v1/auth/users')
        self.assertEqual(result.status_code, 200)

    def test_empty_users_list(self):
        result = self.client.get('/api/v1/auth/users')
        result_data = json.loads(result.data)
        print(result_data)
        self.assertEqual("There are no records", result_data["message"])

    def test_get_user_by_username(self):
        with self.client:
            # REgister a user
            self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='charity marani',
                    email='chacha@gmail.com',
                    role='attendant',
                    username='wanjiru',
                    password='1234',
                    confirm_password='1234'
                )),
                content_type='application/json'
            )
            result = self.client.get('/api/v1/auth/users/wanjiru')
            self.assertEqual(result.status_code, 200)
            # Test user by noexistent username
            result2 = self.client.get('/api/v1/auth/users/amos')
            resp = json.loads(result2.data)
            self.assertEqual(
                "username does not exist in our records", resp["message"])
