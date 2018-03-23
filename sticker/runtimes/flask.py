
from .base import BaseAPI
from ..openapi import OpenAPISpec


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
            for operation in path.operations():
                register = flask_app.route(
                    path.url_path(),
                    methods=[operation.http_method()]
                )
                register(self.wrap_handler(operation.resolve_function()))

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
