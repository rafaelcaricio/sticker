# sticker
Sticker place together your OpenAPI 3.0 spec with your Python functions.

Fun to Write:
```python
from sticker.apps import FlaskApp
app = FlaskApp(filename='myspec.yaml')

def hello():
    return "Hello World!"
```

And Easy to Setup:
```
pip install Flask
FLASK_APP=hello.py flask run
```

Also Easy to Run:
```
sticker run flask myspec.yaml
```
