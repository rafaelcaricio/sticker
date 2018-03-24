from abc import abstractmethod
from typing import Dict, Callable

from ..openapi import OpenAPISpec, SpecPath


class BaseAPI:
    def __init__(self, spec: OpenAPISpec):
        self.spec = spec

    @staticmethod
    def read_file_contents(filename: str):
        with open(filename, encoding='utf-8') as file:
            return file.read()

    def register_routes(self) -> None:
        for path in self.spec.paths():
            self.register_path(path)

    def register_path(self, path: SpecPath) -> None:
        raise NotImplementedError

    def wrap_handler(self, bare_function: Callable):
        def _wrapper(*args, **kwargs):
            params = self.to_python_literals(*args, **kwargs)
            return self.back_to_framework(bare_function(params))
        return _wrapper

    @abstractmethod
    def to_python_literals(self, *args, **kwargs):
        """
        Get flask parameters and build Python literals.

        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def back_to_framework(self, result):
        """
        Returns response values that Flask understand.

        :return:
        """
        raise NotImplementedError


class FlaskLikeAPI(BaseAPI):
    def __init__(self, spec_filename: str, request):
        self.request = request
        self.contents = self.read_file_contents(spec_filename)
        super().__init__(OpenAPISpec(self.contents))

    def register_routes(self) -> None:
        for path in self.spec.paths():
            self.register_path(path)

    def register_path(self, path: SpecPath) -> None:
        method_to_func: Dict[str, Callable] = {}
        for operation in path.operations():
            method_to_func[operation.http_method()] = operation.resolve_function()
        route_path = self.translate_route_format(path)
        view_func = self.wrap_handler(self.route_call_by_http_method(method_to_func))
        self.register_route(
            rule=route_path,
            endpoint=path.url_path(),
            view_func=view_func,
            methods=list(method_to_func.keys())
        )

    @staticmethod
    def translate_route_format(path) -> str:
        return path.url_path().replace('{', '<').replace('}', '>')

    def route_call_by_http_method(self, method_to_func: Dict[str, Callable]) -> Callable:
        def _route(*args, **kwargs):
            return method_to_func[self.request.method](*args, **kwargs)
        return _route

    def to_python_literals(self, *args, **kwargs):
        """
        Get flask parameters and build Python literals.

        :return:
        """
        return {}

    def back_to_framework(self, result):
        """
        Returns response values that Flask understand.

        :return:
        """
        return result.get('content', '')

    @abstractmethod
    def register_route(self, rule, endpoint, view_func, methods):
        raise NotImplementedError

