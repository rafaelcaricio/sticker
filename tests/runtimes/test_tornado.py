import pytest
from textwrap import dedent

from sticker import TornadoAPI
from tornado.testing import AsyncHTTPTestCase


@pytest.mark.usefixtures("simple_api_spec_attr")
class TestHelloApp(AsyncHTTPTestCase):
    def get_app(self):
        return TornadoAPI(self.simple_api_get_spec).get_app()

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body.decode(), 'Hello!')


class APIClientForTestCase(AsyncHTTPTestCase):
    operation_id = NotImplemented

    def get_app(self):
        return self.api_client_for().get_app()

    def api_client_for(self):
        return TornadoAPI(spec_text=dedent("""
        openapi: 3.0.0
        paths:
            /:
                get:
                    operationId: {this_module}.{operation_id}
        """.format(operation_id=self.operation_id, this_module=__name__)))


def handler_set_status_code(params):
    return {"status": 201}


class TestSetStatusCode(APIClientForTestCase):
    operation_id = 'handler_set_status_code'

    def test_set_status_code(self):
        response = self.fetch('/')
        self.assertEqual(201, response.code)
        self.assertEqual('', response.body.decode())


def handler_set_status_and_content(params):
    return {
        "content": '{"id":"123"}',
        "status": 201
    }


class TestSetStatusAndContent(APIClientForTestCase):
    operation_id = 'handler_set_status_and_content'

    def test_set_status_and_content(self):
        response = self.fetch('/')
        self.assertEqual(201, response.code)
        self.assertEqual('{"id":"123"}', response.body.decode())


def handler_set_headers(params):
    return {
        "headers": {
            "Content-Type": "application/json"
        },
        "content": '{"id":"123"}',
        "status": 201
    }


class TestSetHeaders(APIClientForTestCase):
    operation_id = 'handler_set_headers'

    def test_set_headers(self):
        response = self.fetch('/')
        self.assertEqual(201, response.code)
        self.assertEqual('{"id":"123"}', response.body.decode())
        self.assertTrue('Content-Type' in response.headers)
        self.assertEquals('application/json', response.headers['Content-Type'])
