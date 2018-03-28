
from .base import FlaskLikeAPI
from typing import Optional
import bottle


class BottleAPI(FlaskLikeAPI):
    def __init__(self, spec_filename: Optional[str]=None, spec_text: Optional[str]=None):
        super().__init__(spec_filename=spec_filename, spec_text=spec_text, request=bottle.request)

    def run(self, *args, **kwargs):
        self.register_routes()
        return bottle.run(*args, **kwargs)

    def register_route(self, rule, endpoint, view_func, methods):
        bottle.route(rule, methods, view_func)
