<p align="center">
  <img height="100" src="https://s3.amazonaws.com/sticker-github/sticker.png" alt="Sticker Logo">
</p>

> Sticker is the glue between Python functions and your API design.

Execute your API design in OpenAPI 3.0 format with Sticker. Let your Python functions automatically become you API handlers. With sticker you can have either Flask, Sanic, Tornado, and others as your Application runtime.

### It's Easy to Write:
```python
from sticker.runtimes import FlaskApp
app = FlaskApp(filename='hello_api.yml')

def hello():
    return "Hello World!"
```

### And Familiar to Run:
```
pip install Flask
FLASK_APP=hello.py flask run
```

No _glue code_ necessary to bring to life your APIs. All validation, content negotiation, type checking, and mocking is handled at runtime by Sticker.