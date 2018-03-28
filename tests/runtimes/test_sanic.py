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
                operationId: {this_module}.{operation_id}
    """.format(operation_id=operation_id, this_module=__name__)))
    return test_client(api.get_app(__name__))


def handler_set_status_code(params):
    return {"status": 201}


async def test_set_status_code(test_client):
    api_client = await api_client_for('handler_set_status_code', test_client)
    response = await api_client.get('/')
    assert 201 == response.status
    assert '' == (await response.content.read()).decode()


def handler_set_status_code_to_400(params):
    return {"status": 400}


async def test_set_status_code_to_400(test_client):
    api_client = await api_client_for('handler_set_status_code_to_400', test_client)
    response = await api_client.get('/')
    assert 400 == response.status
    assert (await response.content.read()).decode() == ''


def handler_set_status_and_content(params):
    return {
        "content": '{"id":"123"}',
        "status": 201
    }


async def test_set_status_and_content(test_client):
    api_client = await api_client_for('handler_set_status_and_content', test_client)
    response = await api_client.get('/')
    assert response.status == 201
    assert (await response.content.read()).decode() == '{"id":"123"}'


def handler_set_headers(params):
    return {
        "headers": {
            "Content-Type": "application/json"
        },
        "content": '{"id":"123"}',
        "status": 201
    }


async def test_set_headers(test_client):
    api_client = await api_client_for('handler_set_headers', test_client)
    response = await api_client.get('/')
    assert response.status == 201
    assert (await response.content.read()).decode() == '{"id":"123"}'
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json'

