from sticker import FlaskAPI


def say_hello(params):
    return {"contents": "Hello World!"}


api = FlaskAPI('hello.yml')
app = api.get_app(__name__)

if __name__ == '__main__':
    app.run()
