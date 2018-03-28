
from .base import FlaskLikeAPI
from typing import Optional
import flask


class FlaskAPI(FlaskLikeAPI):
    def __init__(self, spec_filename: Optional[str]=None, spec_text: Optional[str]=None):
        super().__init__(spec_filename=spec_filename, spec_text=spec_text, request=flask.request)
        self.app: flask.Flask = None

    def get_app(self, *args, **kwargs) -> flask.Flask:
        self.app = flask.Flask(*args, **kwargs)
        self.register_routes()
        return self.app

    def register_route(self, rule, endpoint, view_func, methods):
        self.app.add_url_rule(
            rule=rule,
            endpoint=endpoint,
            view_func=view_func,
            methods=methods
        )

    def back_to_framework(self, result: dict):
        args = (result.get('content', ''), result.get('status', 200), result.get('headers', {}),)
        return flask.make_response(*args)
