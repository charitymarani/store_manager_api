from unittest import TestCase
from application import create_app
from instance.config import app_config

class BaseTestCase(TestCase):

    def setUp(self):
        self.app = create_app(config="testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """removes the dictionaries and the context"""
        self.app_context.pop()


