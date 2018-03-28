from webtest import TestApp
from textwrap import dedent

from sticker import FlaskAPI


def test_simple(simple_api_get_spec):
    api = FlaskAPI(simple_api_get_spec)
    api_client = TestApp(api.get_app(__name__))

    response = api_client.get('/')
    assert response.status == '200 OK'
    assert response.body.decode() == 'Hello!'


def handler_set_status_code(params):
    return {"status": 201}


def test_set_status_code():
    api = FlaskAPI(spec_text=dedent("""
    openapi: 3.0.0
    paths:
        /:
            get:
                operationId: test_flask.handler_set_status_code
    """))
    api_client = TestApp(api.get_app(__name__))

    response = api_client.get('/')
    assert response.status == '201 CREATED'
    assert response.body.decode() == ''

