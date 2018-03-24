
from .base import BaseAPI
from ..openapi import OpenAPISpec
from typing import Dict, Callable
from flask import request


def flask_handler(method_to_func):
    def _route(*args, **kwargs):
        return method_to_func[request.method](*args, **kwargs)
    return _route


class FlaskAPI(BaseAPI):
    def __init__(self, spec_filename: str):
        self.contents = self.read_file_contents(spec_filename)
        self.spec = OpenAPISpec(self.contents)

    def get_app(self, *args, **kwargs):
        from flask import Flask
        app = Flask(*args, **kwargs)
        self.register_to(app)
        return app

    def register_to(self, flask_app) -> None:
        for path in self.spec.paths():
            method_to_func: Dict[str, Callable] = {}
            for operation in path.operations():
                method_to_func[operation.http_method()] = operation.resolve_function()

            flasked_path = path.url_path().replace('{', '<').replace('}', '>')
            flask_app.add_url_rule(
                rule=flasked_path,
                endpoint=path.url_path(),
                view_func=self.wrap_handler(flask_handler(method_to_func)),
                methods=list(method_to_func.keys())
            )

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
        return result.get('contents', '')
