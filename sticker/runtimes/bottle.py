
from .base import FlaskLikeAPI
from typing import Optional
import bottle


class BottleAPI(FlaskLikeAPI):
    def __init__(self, spec_filename: Optional[str]=None, spec_text: Optional[str]=None):
        super().__init__(spec_filename=spec_filename, spec_text=spec_text, request=bottle.request)
        self.app = bottle.app()

    def run(self, *args, **kwargs):
        self.register_routes()
        return self.app.run(*args, **kwargs)

    def register_route(self, rule, endpoint, view_func, methods):
        self.app.route(rule, methods, view_func)

    def back_to_framework(self, result):
        kwargs = {
            'body': result.get('content', ''),
            'status': result.get('status', 200),
            'headers': result.get('headers', {})
        }
        return bottle.HTTPResponse(**kwargs)
