<p align="center">
  <img height="100" src="https://s3.amazonaws.com/sticker-github/sticker.png" alt="Sticker Logo">
</p>

> Sticker is the glue between Python functions and your API design.

Let your Python functions automatically become your API handlers. Sticker allows you to choose Flask, bottle.py,
Sanic, or Tornado as your application runtime.

Key features:
 - Community created and maintained
 - Support for [__OpenAPI 3.0__](https://swagger.io/specification/)
 - Multi-framework support:
 [__Flask__](http://flask.pocoo.org/),
 [__bottle.py__](https://github.com/bottlepy/bottle),
 [__Sanic__](https://github.com/channelcat/sanic),
 and
 [__Tornado__](http://www.tornadoweb.org/en/stable/)
 - Support for __pure Python handlers__ (no boilerplate code)

### It's Easy to Write:

You need a little bit of Python.

```python
# filename: hello.py

def say_hello(params):
    return {"contents": "Hello World!"}
```

Plus bits of your API description.

```yml
# filename: hello.yml
openapi: "3.0.0"
paths:
  /:
    get:
      operationId: hello.say_hello
```

Now the fun part, you choose which web framework you want to use.

Run with Flask:
```python
from sticker import FlaskAPI
api = FlaskAPI('hello.yml')
api.get_app(__name__).run()
```

Run with Bottle.py:
```python
from sticker import BottleAPI
api = BottleAPI('hello.yml')
api.run()
```

Run with Sanic:
```python
from sticker import SanicAPI
api = SanicAPI('hello.yml')
api.get_app(__name__).run()
```

Run with Tornado:
```python
from sticker import TornadoAPI
import tornado.ioloop
api = TornadoAPI('hello.yml')
api.get_app().listen(8888)
tornado.ioloop.IOLoop.current().start()
```

The framework setup, validation, types conversion, and mocking is handled at runtime by Sticker.

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
specific boilerplate code, including Sticker's itself. This allows you to swap between different frameworks
as you wish. Sticker will take care of putting together your code, your API, and the framework you choose.

```python
def myhandler(params):
    return {
        "content": f"Hello {params.get("name", "World")}!",
        "status": 200
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

As you could see in the example above, no imports from Sticker were necessary to define the API handler function.
This is only possible because Sticker expects your handlers to follow a code convention.

### Anatomy of an API handler function

...

### Responses

API handlers are expected to return a Python dictionary (`dict`) object. The returned dictionary defines how a response
will look like. All keys in the dictionary are optional. The expected keys are described in the table bellow.

Key | Type |  Description
----|------|----
content | str | Body of HTTP request. No treatment/parsing of this value is done. The value is passed directly to the chosen framework.
json | Union[dict, List[dict]] | JSON value to be used in the body of the request. This is a shortcut to having the header "Content-Type: application/json" and serializing this value using the most common way done by the chosen framework.
file | Union[IO[AnyStr], str] | Data to be returned as byte stream. This is a shortcut for having the header "Content-Type: application/octet-stream". Uses the most common way to stream files with the chosen framework.
redirect | str | The path or full URL to be redirected. This is a shortcut for having the header "Location:" with HTTP status `301`.
status | int | The HTTP status code to be used in the response. This value overrides any shortcut default status code.
headers | Dict[str, str] | The HTTP headers to be used in the response. This value is merged with the shortcut values with priority.

We have exposed here some examples of using different configurations of the `dict` we've defined above to describe the
HTTP response of API handlers. The actual HTTP response value generated will vary depending on the framework chosen as
runtime. The examples are a minimal illustration of what to expect to be the HTTP response.

The "content" key can be used when it's desired to return a "Hello world!" string with status `200`.

```python
def say_hello(params):
    return {"content": "Hello world!"}
```

Results in the HTTP response similar to:

```
HTTP/1.1 200 OK
Content-Type: text/plain

Hello world!
```

The "json" key can be used when desired to return an JSON response with status `201`.

```python
def create(params):
    data = {
        "id": "uhHuehuE",
        "value": "something"
    }
    return {"json": data, "status": 201}
```

The HTTP response generated will be similar to:
```
HTTP/1.1 201 Created
Content-Type: application/json

{"id":"uhHuehuE","value":"something"}
```

The "file" key is used to return file contents.

```python
def homepage(params):
    return {
        "file": open('templates/home.html', 'r'),
        "headers": {
            "Content-Type": "text/html"
        }
    }
```

The HTTP response will be similar to:

```
HTTP/1.1 200 OK
Content-Type: text/html

<html><title>My homepage</title><body><h1>Welcome!</h1></body></html>
```

When necessary to redirect request, the "redirect" key can be used.

```python
def old_endpoint(params):
    return {'redirect': '/new-path'}
```

The HTTP response will be similar to:

```
HTTP/1.1 301 Moved Permanently
Location: https://example.com/new-path
```

The usage of keys "status" and "headers" were shown in the previous examples. The "status" and "headers" keys, when set,
override the values set by default when using the shortcut keys ("json", "file", and "redirect").

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
