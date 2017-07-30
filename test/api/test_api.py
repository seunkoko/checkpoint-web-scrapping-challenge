from main import create_flask_app
from test.base import BaseTestCase


class TestApiInitialization(BaseTestCase):

    def test_testing_config(self):
        app = create_flask_app('testing')
        self.assertTrue(app.config.get('TESTING'))
