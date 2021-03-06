import asyncio

from typing import Callable, Dict, Optional
from sanic import Sanic, response

from .base import FlaskLikeAPI


class SanicAPI(FlaskLikeAPI):
    def __init__(self, spec_filename: Optional[str]=None, spec_text: Optional[str]=None):
        super().__init__(spec_filename=spec_filename, spec_text=spec_text)
        self.app: Sanic = None

    def get_app(self, *args, **kwargs):
        self.app = Sanic(*args, **kwargs)
        self.register_routes()
        return self.app

    def register_route(self, rule, endpoint, view_func, methods):
        self.app.route(uri=rule, methods=methods, name=endpoint)(view_func)

    def wrap_handler(self, bare_function: Callable):
        if asyncio.iscoroutine(bare_function):
            async def _wrapper(request, *args, **kwargs):
                params = self.to_python_literals(request, *args, **kwargs)
                return self.back_to_framework(await bare_function(params))
        else:
            def _wrapper(request, *args, **kwargs):
                params = self.to_python_literals(request, *args, **kwargs)
                return self.back_to_framework(bare_function(params))
        return _wrapper

    def route_call_by_http_method(self, method_to_func: Dict[str, Callable]) -> Callable:
        def _route(request, *args, **kwargs):
            return method_to_func[request.method](request, *args, **kwargs)
        return _route

    def to_python_literals(self, request, *args, **kwargs):
        return {}

    def back_to_framework(self, result):
        return response.text(result.get('content', ''),
                             status=result.get('status', 200),
                             headers=result.get('headers', {}))
