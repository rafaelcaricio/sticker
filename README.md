<p align="center">
  <img height="100" src="https://s3.amazonaws.com/sticker-github/sticker.png" alt="Sticker Logo">
</p>

> Sticker is the glue between Python functions and your API design.

Let your Python functions automatically become you API handlers. Sticker allows you to choose Flask,
Sanic, or Tornado as your application runtime.

Key features:
 - Community created and maintained
 - Support for [__OpenAPI 3.0__](https://swagger.io/specification/)
 - Multi-framework support:
 [__Flask__](http://flask.pocoo.org/),
 [__Sanic__](https://github.com/channelcat/sanic),
 and
 [__Tornado__](http://www.tornadoweb.org/en/stable/)
 - Support for __pure Python handlers__ (no boilerplate code)

### It's Easy to Write:
You need a little bit of Python.
```python
def say_hello(params):
    return {"content": "Hello World!"}

# filename: hello.py
```
Plus bits of specification.
```yml
openapi: "3.0.0"
paths:
  /:
    get:
      operationId: say_hello

# filename: hello.yml
```

Finally we _sticker_ it together.
```
pip install sticker Flask
sticker run flask hello.yml
```

No _glue code_ necessary to bring to life your API. All validation, content negotiation, type checking, and mocking is handled at runtime by Sticker.

✨

# Installation

Sticker is published at PyPI, so you can use `pip` to install:

```
pip install sticker
```

# Requirements

Sticker was developed for __Python >=3.6__ and __OpenAPI 3.0__. Support for Python 2.7 is not present nor planned for this project.

# Documentation

Sticker is a flexible metaframework for Web API development and execution. The OpenAPI 3.0 standard is used as
description format for Sticker powered APIs. You provide the API specification and choose one of the
Sticker's runtimes to have a webserver up and running.

In this document we will describe a few different ways to write code that works well with Sticker.

## Pure Python Handlers

Sticker supports the use of pure Python functions as handlers. Your code will be free of any framework
specific boilerplate code. This allows you to swap between different frameworks as you wish. Sticker will
take care of putting together your code, your API, and the framework you choose.

```python
def myhandler(params):
    return {
        "content": f"Hello {params.get("name", "World")}!",
        "status_code": 200
    }
```

Writing tests for pure Python handles is easy and also
free of boilerplate code.

```python
def test_myhandler():
    params = {
        "name": "John Doe"
    }
    response = myhandler(params)
    assert response["content"] == "Hello John Doe!"
```

## Error Handling

Sticker expects you to define the error format to be returned by your API. A error handler is configurable,
and called every time validation for the endpoint fails.

```python
def error_handler(error):
    return {
        "content": {
            "error": error["message"]
        },
        "headers": {
            "Content-Type": "application/json"
        },
        "status_code": 400
    }
```