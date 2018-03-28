from webtest import TestApp
from textwrap import dedent

from sticker import BottleAPI


def test_simple(simple_api_get_spec):
    api = BottleAPI(simple_api_get_spec)
    api.register_routes()
    api_client = TestApp(api.app)

    response = api_client.get('/')
    assert response.status == '200 OK'
    assert response.body.decode() == 'Hello!'


def api_client_for(operation_id):
    api = BottleAPI(spec_text=dedent("""
    openapi: 3.0.0
    paths:
        /:
            get:
                operationId: handlers.{operation_id}
    """.format(operation_id=operation_id)))
    api.register_routes()
    api_client = TestApp(api.app)
    return api_client


def test_set_status_code():
    client = api_client_for('handler_set_status_code')
    response = client.get('/')
    assert response.status == '201 Created'
    assert response.body.decode() == ''


def test_set_status_and_content():
    response = api_client_for('handler_set_status_and_content').get('/')
    assert response.status == '201 Created'
    assert response.body.decode() == '{"id":"123"}'


def test_set_headers():
    response = api_client_for('handler_set_headers').get('/')
    assert response.status == '201 Created'
    assert response.body.decode() == '{"id":"123"}'
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json'
