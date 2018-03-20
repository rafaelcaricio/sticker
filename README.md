<p align="center">
  <img height="100" src="https://s3.amazonaws.com/sticker-github/sticker.png" alt="Sticker Logo">
</p>

> Sticker is the glue between Python functions and your API design.

Execute your API design in OpenAPI 3.0 format with Sticker. Let your Python functions automatically become you API handlers. Sticker allows you to choose either Flask, Sanic, Tornado as your application runtime.

### It's Easy to Write:
```python
from sticker.runtimes import FlaskApp
app = FlaskApp(filename='hello_api.yml')

def hello():
    return "Hello World!"
```

### And Familiar to Run:
```
pip install sticker Flask
FLASK_APP=hello.py flask run
```

No _glue code_ necessary to bring to life your APIs. All validation, content negotiation, type checking, and mocking is handled at runtime by Sticker.

# Installation

Sticker is published at PyPI, so you can use `pip` to install:

```
pip install sticker
```

# Requirements

Sticker was developed for __Python >=3.6__ and __OpenAPI 3.0__. Support for Python 2.7 is not present nor planned for this project.