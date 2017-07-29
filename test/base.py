from flask_testing import TestCase

from main import create_flask_app


class BaseTestCase(TestCase):
    
    def create_app(self):
        self.app = create_flask_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        return self.app

    def setUp(self):
        pass

    def tearDown(self):
        self.app_context.pop()