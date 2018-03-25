
from sticker import TornadoAPI
from tornado.testing import AsyncHTTPTestCase
from tests.conftest import simple_api_get_spec


class TestHelloApp(AsyncHTTPTestCase):
    def get_app(self):
        return TornadoAPI(simple_api_get_spec()).get_app()

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body.decode(), 'Hello!')
