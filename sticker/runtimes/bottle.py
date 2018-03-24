
from .base import FlaskLikeAPI
import bottle


class BottleAPI(FlaskLikeAPI):
    def __init__(self, spec_filename: str):
        super().__init__(spec_filename, bottle.request)

    def run(self, *args, **kwargs):
        self.register_routes()
        return bottle.run(*args, **kwargs)

    def register_route(self, rule, endpoint, view_func, methods):
        bottle.route(rule, methods, view_func)
