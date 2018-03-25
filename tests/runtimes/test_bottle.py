from webtest import TestApp

from sticker import BottleAPI
from sticker.runtimes.bottle import bottle


def test_simple(simple_api_get_spec):
    api = BottleAPI(simple_api_get_spec)
    api.register_routes()
    api_client = TestApp(bottle.app())

    response = api_client.get('/')
    assert response.status == '200 OK'
    assert response.body.decode() == 'Hello!'
