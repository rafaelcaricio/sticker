import pytest
from sticker import SanicAPI
from textwrap import dedent


async def test_simple(test_client, simple_api_get_spec):
    api = SanicAPI(simple_api_get_spec)
    api_client = await test_client(api.get_app(__name__))

    response = await api_client.get('/')
    assert 200 == response.status
    assert 'Hello!' == (await response.content.read()).decode()


def api_client_for(operation_id, test_client):
    api = SanicAPI(spec_text=dedent("""
    openapi: 3.0.0
    paths:
        /:
            get:
                operationId: handlers.{operation_id}
    """.format(operation_id=operation_id)))
    return test_client(api.get_app(__name__))


async def test_set_status_code(test_client):
    api_client = await api_client_for('handler_set_status_code', test_client)
    response = await api_client.get('/')
    assert 201 == response.status
    assert '' == (await response.content.read()).decode()


async def test_set_status_code_to_400(test_client):
    api_client = await api_client_for('handler_set_status_code_to_400', test_client)
    response = await api_client.get('/')
    assert 400 == response.status
    assert (await response.content.read()).decode() == ''


async def test_set_status_and_content(test_client):
    api_client = await api_client_for('handler_set_status_and_content', test_client)
    response = await api_client.get('/')
    assert 201 == response.status
    assert '{"id":"123"}' == (await response.content.read()).decode()


async def test_set_headers(test_client):
    api_client = await api_client_for('handler_set_headers', test_client)
    response = await api_client.get('/')
    assert 201 == response.status
    assert '{"id":"123"}' == (await response.content.read()).decode()
    assert 'Content-Type' in response.headers
    assert 'application/json' == response.headers['Content-Type']

