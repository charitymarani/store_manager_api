from unittest import TestCase
from application import create_app
from instance.config import app_config
from ...api.v1.models import (USERS_LIST,SALES_LIST,PRODUCTS_LIST)

class BaseTestCase(TestCase):

    def setUp(self):
        self.app = create_app(config="testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        

    def tearDown(self):
        """removes the dictionaries and the context"""
        del USERS_LIST[:]
        del SALES_LIST[:]
        del PRODUCTS_LIST[:]
        
