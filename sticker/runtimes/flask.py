
from .base import FlaskLikeAPI
import flask


class FlaskAPI(FlaskLikeAPI):
    def __init__(self, spec_filename: str):
        super().__init__(spec_filename, flask.request)
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
