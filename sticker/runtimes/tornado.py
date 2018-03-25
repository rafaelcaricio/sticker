from typing import List, Dict, Callable
import re

import tornado.web

from .base import BaseAPI
from ..openapi import SpecPath, SpecOperation


class TornadoAPI(BaseAPI):
    def __init__(self, spec_filename: str):
        super().__init__(spec_filename)
        self.routes: List = None

    def get_app(self, *args, **kwargs):
        self.routes = []
        self.register_routes()
        return tornado.web.Application(self.routes, *args, **kwargs)

    def register_path(self, path: SpecPath) -> None:
        kwargs = {
            'api': self,
            'operations': path.operations()
        }
        path_regex = self.to_regex(path.url_path())
        self.routes.append((path_regex, GenericHandler, kwargs))

    @staticmethod
    def to_regex(path: str) -> str:
        return re.sub(r'{([^}]+)}', r'(?P<\1>[^/]+)', path)

    def wrap_handler(self,
                     handler: tornado.web.RequestHandler,
                     operation: SpecOperation,
                     bare_function: Callable):
        def _wrapper(*args, **kwargs):
            params = self.to_python_literals(handler, operation, *args, **kwargs)
            return self.back_to_framework(handler, operation, bare_function(params))
        return _wrapper

    def to_python_literals(
            self,
            handler: tornado.web.RequestHandler,
            operation: SpecOperation,
            *args,
            **kwargs
    ):
        return {}

    def back_to_framework(
            self,
            handler: tornado.web.RequestHandler,
            operation: SpecOperation,
            result
    ):
        handler.write(result.get('content', ''))
        handler.finish()


class GenericHandler(tornado.web.RequestHandler):
    api: TornadoAPI = None
    operations_hash: Dict[str, Callable] = None

    def initialize(self, api: TornadoAPI, operations: List[SpecOperation]):
        self.api = api
        self.operations_hash = {}
        for operation in operations:
            handler = api.wrap_handler(
                handler=self,
                operation=operation,
                bare_function=operation.resolve_function()
            )
            self.operations_hash[operation.http_method()] = handler

    def call_method_or_super(self, method: str, *args, **kwargs):
        if method.upper() not in self.operations_hash:
            return getattr(super(), method.lower())(*args, **kwargs)
        return self.operations_hash[method.upper()](*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.call_method_or_super('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.call_method_or_super('post', *args, **kwargs)

