from sticker import FlaskAPI


def say_hello(params):
    return {"content": "Hello World!"}


if __name__ == '__main__':
    api = FlaskAPI('hello.yml')
    api.get_app(__name__).run()
