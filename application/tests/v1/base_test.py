from unittest import TestCase
from application import create_app
from instance.config import app_config
from ...api.v1.models import (USERS_DICT,SALES_DICT,PRODUCTS_DICT)


class BaseTestCase(TestCase):

    def setUp(self):
        self.app = create_app(config="testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        

    def tearDown(self):
        """removes the dictionaries and the context"""
        del USERS_DICT[:]
        del SALES_DICT[:]
        del PRODUCTS_DICT[:]
        
