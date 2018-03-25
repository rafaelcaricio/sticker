from webtest import TestApp

from sticker import FlaskAPI


def test_simple(simple_api_get_spec):
    api = FlaskAPI(simple_api_get_spec)
    api_client = TestApp(api.get_app(__name__))

    response = api_client.get('/')
    assert response.status == '200 OK'
    assert response.body.decode() == 'Hello!'
